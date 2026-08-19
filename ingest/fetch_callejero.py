"""
Ingest: Callejero Municipal de Las Palmas de Gran Canaria.
Source: ArcGIS REST API — sit.laspalmasgc.es
Layer: CALLEJERO.CA_V_TRA_TRAMOS (5.305 segmentos viales)
Output: parquet/geografia/callejero_lpgc.parquet
"""
import os
import json
import pandas as pd
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "geografia")
os.makedirs(OUT, exist_ok=True)

QUERY_URL = ("https://sit.laspalmasgc.es/server/rest/services/opendata/"
             "callejero/MapServer/0/query")

print("\n=== Callejero Municipal LPGC ===")

all_features = []
offset = 0
limit = 1000

while True:
    params = {
        "where": "1=1",
        "outFields": "OBJECTID,CLV_DS_ABR_NOMCAL,TPA_DS_DENOMINACION,HVIA_DS_DENOMINACION,SHAPE_Length",
        "returnGeometry": "true",
        "f": "geojson",
        "resultOffset": offset,
        "resultRecordCount": limit,
    }
    try:
        data = fetch_json(QUERY_URL, params=params, timeout=60)
    except Exception as e:
        print(f"  x Error at offset {offset}: {e}")
        break

    features = data.get("features", [])
    if not features:
        break

    all_features.extend(features)
    offset += limit
    print(f"  Downloaded: {len(all_features)} segmentos", end="\r")

print(f"\n  Total: {len(all_features)} segmentos")

if not all_features:
    print("  x No data downloaded")
    exit(1)

# Convert to DataFrame
rows = []
for f in all_features:
    props = f.get("properties", {})
    rows.append({
        "objectid": props.get("OBJECTID"),
        "tipo_via": props.get("CLV_DS_ABR_NOMCAL"),
        "particula": props.get("TPA_DS_DENOMINACION"),
        "nombre_via": props.get("HVIA_DS_DENOMINACION"),
        "longitud_m": props.get("SHAPE_Length"),
    })

df = pd.DataFrame(rows)

# Build full street name
df["via_completa"] = df.apply(
    lambda r: " ".join(filter(None, [str(r["tipo_via"]) if pd.notna(r["tipo_via"]) else None,
                                      str(r["particula"]) if pd.notna(r["particula"]) else None,
                                      str(r["nombre_via"]) if pd.notna(r["nombre_via"]) else None])),
    axis=1
)

out_path = os.path.join(OUT, "callejero_lpgc.parquet")
df.to_parquet(out_path, index=False)
print(f"\n  -> Saved: {out_path} ({len(df)} rows)")
print(f"\n  --- Muestra ---")
print(f"  Tipos de via: {df['tipo_via'].value_counts().head(10).to_dict()}")
print(f"  Vias unicas: {df['via_completa'].nunique()}")

print("\nDone.")
