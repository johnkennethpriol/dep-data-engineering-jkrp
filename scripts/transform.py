"""
Phase 3 — Data Transformation
Loads raw OpenAQ PM2.5 pulls for Manila and Ortigas, combines them into
one dataset with station identity preserved, validates each record, and
writes both the cleaned data and a plain-text cleaning log to
data/processed/. Flags and logs issues rather than silently dropping them.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    {"file": "openaq_ncr_pm25_manila_2026-09-13.json", "station": "manila", "instrument": "government_reference"},
    {"file": "openaq_ncr_pm25_ortigas_2026-09-13.json", "station": "ortigas", "instrument": "low_cost_clarity"},
]

MIN_PLAUSIBLE = 0
MAX_PLAUSIBLE = 500  # µg/m³ ceiling; readings above this are treated as sensor fault, not real air quality


def load_source(filename, station, instrument):
    path = RAW_DIR / filename
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for r in data["results"]:
        rows.append({
            "station": station,
            "instrument": instrument,
            "timestamp_utc": r.get("period", {}).get("datetimeFrom", {}).get("utc"),
            "value": r.get("value"),
        })
    return pd.DataFrame(rows)


def transform():
    log_lines = [f"Cleaning run: {datetime.utcnow().isoformat()}Z", ""]

    frames = []
    for source in SOURCES:
        df = load_source(source["file"], source["station"], source["instrument"])
        raw_count = len(df)
        log_lines.append(f"{source['station']}: loaded {raw_count} raw records from {source['file']}")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    total_raw = len(combined)

    # Timestamp parsing
    combined["timestamp_utc"] = pd.to_datetime(combined["timestamp_utc"], utc=True, errors="coerce")
    bad_timestamp = combined["timestamp_utc"].isna()
    log_lines.append(f"Unparseable timestamps: {bad_timestamp.sum()}")

    # Null values
    bad_value = combined["value"].isna()
    log_lines.append(f"Null values: {bad_value.sum()}")

    # Physically impossible negative readings
    negative = combined["value"] < MIN_PLAUSIBLE
    log_lines.append(f"Negative values (physically impossible): {negative.sum()}")

    # Implausibly high readings, likely sensor fault
    too_high = combined["value"] > MAX_PLAUSIBLE
    log_lines.append(f"Values above {MAX_PLAUSIBLE} µg/m³ (flagged as likely sensor fault): {too_high.sum()}")
    if too_high.sum() > 0:
        flagged = combined[too_high][["station", "timestamp_utc", "value"]]
        log_lines.append("  Flagged records:")
        for _, row in flagged.iterrows():
            log_lines.append(f"    {row['station']} | {row['timestamp_utc']} | {row['value']}")

    # Duplicate timestamp+station pairs
    dupes = combined.duplicated(subset=["station", "timestamp_utc"], keep="first")
    log_lines.append(f"Duplicate (station, timestamp) pairs: {dupes.sum()}")

    # Build the clean dataset: drop bad timestamps, nulls, negatives, and duplicates.
    # Keep the too-high values IN the dataset but flagged, rather than silently
    # dropping them, they're a judgment call for analysis, not an ingestion error.
    drop_mask = bad_timestamp | bad_value | negative | dupes
    cleaned = combined[~drop_mask].copy()
    cleaned["flagged_high"] = cleaned["value"] > MAX_PLAUSIBLE

    cleaned = cleaned.sort_values(["station", "timestamp_utc"]).reset_index(drop=True)

    log_lines.append("")
    log_lines.append(f"Total raw records (both stations): {total_raw}")
    log_lines.append(f"Total records dropped: {drop_mask.sum()}")
    log_lines.append(f"Total records in cleaned dataset: {len(cleaned)}")
    log_lines.append(f"  of which flagged as likely sensor fault (kept, not dropped): {cleaned['flagged_high'].sum()}")
    for station in cleaned["station"].unique():
        subset = cleaned[cleaned["station"] == station]
        log_lines.append(f"  {station}: {len(subset)} records, {subset['timestamp_utc'].min()} to {subset['timestamp_utc'].max()}")

    output_csv = PROCESSED_DIR / "ncr_pm25_cleaned.csv"
    cleaned.to_csv(output_csv, index=False)
    log_lines.append("")
    log_lines.append(f"Saved cleaned dataset to {output_csv}")

    log_path = PROCESSED_DIR / "cleaning_log.txt"
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print("\n".join(log_lines))
    print(f"\nCleaning log saved to {log_path}")


if __name__ == "__main__":
    transform()