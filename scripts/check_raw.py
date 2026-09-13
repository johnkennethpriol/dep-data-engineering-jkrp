import json

with open("data/raw/openaq_ncr_pm25_ortigas_2026-09-13.json", encoding="utf-8") as f:
    data = json.load(f)

values = [r["value"] for r in data["results"] if r.get("value") is not None]
print(f"count: {len(values)}")
print(f"min: {min(values)}, max: {max(values)}, mean: {sum(values)/len(values):.3f}")