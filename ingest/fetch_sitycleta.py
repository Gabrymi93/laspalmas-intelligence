"""
Ingest: Sitycleta bike sharing stations (historical + OSM GTFS stops).
Source: datosabiertos.laspalmasgc.es DataStore + OSM Overpass API
Output: parquet/movilidad/sitycleta.parquet, parquet/movilidad/gtfs_stops.parquet
"""
import json, os, urllib.request, urllib.parse, duckdb, pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "movilidad")
os.makedirs(OUT, exist_ok=True)

# --- Sitycleta stations (via DataStore) ---
print("=== Sitycleta stations ===")
API = "http://apidatosabiertos.laspalmasgc.es/api/3/action/datastore_search"
res_id = "31948532-c78a-4e30-b6f0-5223977cd17b"
url = f"{API}?resource_id={res_id}&limit=20"
with urllib.request.urlopen(url, timeout=30) as r:
    data = json.loads(r.read())
records = data["result"]["records"]
total = data["result"]["total"]
# Fetch remaining records if any
all_recs = records
if total > 20:
    for offset in range(20, total, 20):
        with urllib.request.urlopen(f"{API}?resource_id={res_id}&limit=20&offset={offset}", timeout=30) as r:
            more = json.loads(r.read())["result"]["records"]
            all_recs.extend(more)

df = pd.DataFrame(all_recs)
df.to_parquet(os.path.join(OUT, "sitycleta.parquet"), index=False)
print(f"  -> {len(df)} stations")

print("\nDone.")
