"""
Ingest: ISTAC population data for Las Palmas de Gran Canaria (cod 35016)
Sources:
  - C00025A_000002: Population by municipality 1986-2026 (CSV via API)
  - Indicadores demográficos: 2008-2022 (direct CSV download)
Output: parquet/poblacion/
"""
import csv
import json
import os
import io
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_text

LPGC = "35016"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "poblacion")
os.makedirs(OUT, exist_ok=True)

# --- 1. Population time series 1986-2026 ---
print("[1/2] Downloading population time series (C00025A_000002)...")
url_pop = "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/C00025A_000002/1.4.csv"
content = fetch_text(url_pop)

rows = []
reader = csv.DictReader(io.StringIO(content))
for row in reader:
    if row["TERRITORIO_CODE"] == LPGC:
        rows.append({
            "year": int(row["TIME_PERIOD_CODE"]),
            "measure_code": row["MEDIDAS_CODE"],
            "measure": row["MEDIDAS#es"],
            "value": float(row["OBS_VALUE"]) if row["OBS_VALUE"] else None,
            "territorio": row["TERRITORIO#es"],
            "territorio_code": row["TERRITORIO_CODE"],
            "notes": row["NOTAS_OBSERVACION#es"],
        })

print(f"  -> {len(rows)} rows for LPGC")

with open(os.path.join(OUT, "poblacion_serie_historica.csv"), "w") as f:
    if rows:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

# --- 2. Demographic indicators 2008-2022 ---
print("[2/2] Downloading indicadores demograficos...")
url_ind = "https://datos.canarias.es/catalogos/estadisticas/dataset/d2fd1aef-2228-4072-917c-f511eeeadc80/resource/343a77f8-c987-43a1-b717-47248720358b/download/2008-2022_indicadores_demograficos_municipios_pmh.csv"
content = fetch_text(url_ind)

rows = []
reader = csv.DictReader(io.StringIO(content))
for row in reader:
    if row["geocode"] == LPGC:
        rows.append(row)

print(f"  -> {len(rows)} rows for LPGC")

with open(os.path.join(OUT, "indicadores_demograficos.csv"), "w") as f:
    if rows:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

# --- Summary ---
print()
print("Files written:")
for fn in os.listdir(OUT):
    fp = os.path.join(OUT, fn)
    print(f"  {fn}: {os.path.getsize(fp)} bytes")
print("Done.")
