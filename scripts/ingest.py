"""
Phase 2 — Data Ingestion
Pulls raw OpenAQ PM2.5 measurement data for an NCR sensor and saves it,
untouched, to data/raw/. No cleaning, no transformation, no reshaping.
"""

import os
import requests
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def ingest():
    api_key = os.environ["OPENAQ_API_KEY"]
    sensor_id = "14258134"  # Ayala MRT, NCR — pm25
    source_name = "openaq_ncr_pm25"
    output_file = RAW_DIR / f"{source_name}_{date.today().isoformat()}.json"

    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers, params={"limit": 1000})
    response.raise_for_status()

    output_file.write_text(response.text, encoding="utf-8")
    print(f"Saved raw data for {source_name} to {output_file}")


if __name__ == "__main__":
    ingest()
