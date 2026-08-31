"""
Ingest: ISTAC viviendas vacacionales LPGC (C00065A_000061)
Granularidad: municipio, mensual
Periodo: 2019-01 → presente
Medidas: viviendas disponibles/reservadas, plazas, estancia media, ingresos
Output: parquet/turismo/vivienda_vacacional_lpgc.parquet
"""
import csv
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_text

LPGC = "35016"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "turismo")
os.makedirs(OUT, exist_ok=True)

url = "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/C00065A_000061/1.27.tsv"
print(f"Downloading viviendas vacacionales...")
content = fetch_text(url)

rows = []
reader = csv.DictReader(content.splitlines(), delimiter="\t")
for row in reader:
    if row["TERRITORIO_CODE"] == LPGC:
        rows.append(row)

print(f"  -> {len(rows)} rows for LPGC")

# Save CSV
csv_path = os.path.join(OUT, "vivienda_vacacional_lpgc.csv")
with open(csv_path, "w") as f:
    if rows:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
print(f"  -> Saved {csv_path}")

print("Done.")
