"""
Ingest: ISTAC employment data for Las Palmas de Gran Canaria (35016)
Sources:
  - E59021A_000008: Paro registrado por sexo y grupo de edad (2008-03 → presente, mensual)
  - E59021A_000011: Paro registrado por sexo y ocupacion (2011-02 → presente, mensual)
Output: parquet/empleo/
"""
import urllib.request
import csv
import os

LPGC = "35016"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "empleo")
os.makedirs(OUT, exist_ok=True)

datasets = [
    {
        "name": "paro_sexo_edad",
        "url": "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E59021A_000008/1.59.csv",
        "desc": "Paro registrado por sexo y grupo de edad (2008-03 → presente)"
    },
    {
        "name": "paro_sexo_ocupacion",
        "url": "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/E59021A_000011/1.60.csv",
        "desc": "Paro registrado por sexo y ocupacion (2011-02 → presente)"
    },
]

for ds in datasets:
    print(f"[{ds['name']}] Downloading {ds['desc']}...")
    response = urllib.request.urlopen(ds["url"])
    content = response.read().decode("utf-8")

    rows = []
    reader = csv.DictReader(content.splitlines())
    for row in reader:
        if row["TERRITORIO_CODE"] == LPGC:
            rows.append(row)

    print(f"  -> {len(rows)} rows for LPGC")

    csv_path = os.path.join(OUT, f"{ds['name']}.csv")
    with open(csv_path, "w") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"  -> Saved {csv_path}")

print("Done.")
