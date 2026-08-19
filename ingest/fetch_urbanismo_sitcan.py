"""
Ingest: SITCAN urban planning data for Las Palmas de Gran Canaria.
Source: opendata.sitcan.es — SIPU resources from planeamiento urbanístico
Output: parquet/urbanismo/ (GeoParquet)
"""
import json
import os
import sys
import zipfile
import shutil
import duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_json, fetch_bytes

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "urbanismo")
os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/sitcan_urbanismo"
os.makedirs(TMP, exist_ok=True)

def log(msg):
    print(msg, flush=True)

log("[fetch] Getting SIPU resources from CKAN...")
url = "https://opendata.sitcan.es/api/3/action/package_show?id=6c933d1e-843d-417a-93ab-aafa95fefdd4"
data = fetch_json(url, timeout=30)

resources = [res for res in data["result"]["resources"] if res.get("format") == "SIPU"]
resources.sort(key=lambda x: x.get("size") or 0)
log(f"[fetch] Found {len(resources)} SIPU resources, total size: {sum(r.get('size',0) for r in resources):,}B")

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")

n_ok = 0
n_skip = 0
for res in resources:
    rid = res["id"]
    name = res.get("name", "?")[:60]
    size = res.get("size") or 0

    # Check if already downloaded
    expected = [os.path.join(OUT, f"{rid[:8]}_{layer}.parquet") for layer in ["AMB", "CAT", "ZUSO"]]
    existing = [p for p in expected if os.path.exists(p)]
    if len(existing) == len(expected):
        n_skip += 1
        continue
    elif existing:
        # Partial: remove incomplete files and re-download
        for p in existing:
            os.remove(p)

    log(f"\n[{rid[:8]}] {name} ({size/1000:.0f} KB)")

    # Download
    zip_path = os.path.join(TMP, f"{rid}.zip")
    try:
        with open(zip_path, "wb") as f:
            f.write(fetch_bytes(res["url"], timeout=120))
    except Exception as e:
        log(f"  ✗ download: {e}")
        continue

    # Extract
    extract_dir = os.path.join(TMP, rid)
    os.makedirs(extract_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir)
    except Exception as e:
        log(f"  ✗ extract: {e}")
        shutil.rmtree(extract_dir, ignore_errors=True)
        os.remove(zip_path)
        continue

    # Convert SHP layers
    layers_found = 0
    for layer in ["AMB", "CAT", "ZUSO"]:
        shp = os.path.join(extract_dir, "02SIST", f"{layer}.shp")
        if not os.path.exists(shp):
            continue
        parquet = os.path.join(OUT, f"{rid[:8]}_{layer}.parquet")
        try:
            con.execute(f"COPY (SELECT * FROM ST_Read('{shp}')) TO '{parquet}' (FORMAT PARQUET)")
            rows = con.execute(f"SELECT count(*) FROM '{parquet}'").fetchone()[0]
            log(f"  ✓ {layer}: {rows} features")
            layers_found += 1
        except Exception as e:
            log(f"  ✗ {layer}: {e}")

    if layers_found == 0:
        log(f"  ✗ no SHP layers found")
    else:
        n_ok += 1

    # Cleanup
    shutil.rmtree(extract_dir, ignore_errors=True)
    os.remove(zip_path)

log(f"\nDone: {n_ok} downloaded, {n_skip} skipped (already present)")

log(f"\nDone: {n_ok}/{len(resources)} resources processed")
con.close()
