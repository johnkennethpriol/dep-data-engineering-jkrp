"""
Phase 2 — Data Ingestion
Pulls raw OpenAQ PM2.5 measurements for each configured NCR sensor,
one calendar month at a time, and saves the untouched API response
to data/raw/. Writes to disk after every month so a failure partway
through does not lose already-pulled data. No cleaning, no transformation.
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import date, datetime, timezone
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    {
        "sensor_id": "6909373",
        "source_name": "openaq_ncr_pm25_manila",
        "date_from": "2023-09-06T21:00:00Z",
        "note": "AirNow government reference monitor, dead since 2026-02-05",
    },
    {
        "sensor_id": "10253230",
        "source_name": "openaq_ncr_pm25_ortigas",
        "date_from": "2024-08-13T00:00:00Z",
        "note": "Clarity low-cost sensor, currently live",
    },
]

MAX_RETRIES = 5


def month_windows(start, end):
    cursor = start
    while cursor < end:
        if cursor.month == 12:
            nxt = cursor.replace(year=cursor.year + 1, month=1)
        else:
            nxt = cursor.replace(month=cursor.month + 1)
        yield cursor, min(nxt, end)
        cursor = nxt


def get_with_retry(url, headers, params):
    for attempt in range(MAX_RETRIES):
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response
        wait = 2 * (attempt + 1)
        print(f"    Got {response.status_code}, retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES})")
        time.sleep(wait)
    response.raise_for_status()
    return response


def save_progress(output_file, sensor_id, source_name, all_results):
    output_file.write_text(
        json.dumps(
            {
                "results": all_results,
                "meta": {
                    "sensor_id": sensor_id,
                    "source_name": source_name,
                    "pulled_at": datetime.utcnow().isoformat(),
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def ingest_one(api_key, sensor_id, source_name, date_from_str):
    headers = {"X-API-Key": api_key}
    base_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
    output_file = RAW_DIR / f"{source_name}_{date.today().isoformat()}.json"

    start = datetime.fromisoformat(date_from_str.replace("Z", "+00:00"))
    end = datetime.now(timezone.utc)

    all_results = []
    for window_start, window_end in month_windows(start, end):
        params = {
            "datetime_from": window_start.isoformat(),
            "datetime_to": window_end.isoformat(),
            "limit": 1000,
            "page": 1,
        }
        response = get_with_retry(base_url, headers, params)
        results = response.json().get("results", [])
        all_results.extend(results)
        print(f"  {window_start.date()} to {window_end.date()}: {len(results)} records (running total: {len(all_results)})")

        save_progress(output_file, sensor_id, source_name, all_results)
        time.sleep(0.3)

    print(f"  Done. Saved {len(all_results)} total records to {output_file}")
    return len(all_results)


def ingest():
    api_key = os.environ["OPENAQ_API_KEY"]
    for source in SOURCES:
        print(f"Pulling {source['source_name']} ({source['note']})...")
        ingest_one(api_key, source["sensor_id"], source["source_name"], source["date_from"])


if __name__ == "__main__":
    ingest()