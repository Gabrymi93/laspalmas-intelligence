"""
Fetch GTFS Guaguas Municipales via CKAN DataStore API (apidatosabiertos.laspalmasgc.es)
Source: http://apidatosabiertos.laspalmasgc.es (CKAN DataStore API)
Output: parquet/movilidad/gtfs_*.parquet
"""
import time
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "movilidad")
os.makedirs(OUT, exist_ok=True)

CKAN = "http://apidatosabiertos.laspalmasgc.es/api/3/action"

GTFS = {
    "1fef4753-4749-4930-8b4f-e7e137729e29": "routes",
    "f58eebdc-96c4-4c35-b1af-cf8efa8fa391": "calendar",
    "494ad441-e208-4626-b67a-87999113f54f": "calendar_exceptions",
    "699f0aa3-6d06-4452-b19e-cd81358b5eab": "trips",
    "7be8d5b4-76b5-4da2-a9c1-60877100cc5f": "stop_times",
}

def fetch_all(rid, name):
    rows = []
    offset = 0
    limit = 32000
    while True:
        data = fetch_json(f"{CKAN}/datastore_search", params={
            "resource_id": rid, "limit": limit, "offset": offset
        }, timeout=30)["result"]
        records = data.get("records", [])
        if not records:
            break
        rows.extend(records)
        offset += limit
        print(f"  {name}: {len(rows)}/{data.get('total','?')}", end="\r")
        if len(records) < limit:
            break
        time.sleep(0.3)
    print(f"\n  -> {len(rows)} rows")
    return pd.DataFrame(rows)

for rid, name in GTFS.items():
    print(f"[gtfs_{name}]")
    df = fetch_all(rid, name)
    if df is not None and len(df) > 0:
        cols = [c for c in df.columns if not c.startswith("_")]
        df[cols].to_parquet(os.path.join(OUT, f"gtfs_{name}.parquet"), index=False)

print("Done.")
