"""
Ingest: Atestados Policia Local (traffic accidents with injuries).
Source: datosabiertos.laspalmasgc.es — CSV direct download
Years: 1998-2016, three tables per year: accidentes, heridos, vehiculos
Output: parquet/movilidad/atestados_{acc,her,veh}.parquet
"""
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import get_csv_df

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "movilidad")
os.makedirs(OUT, exist_ok=True)

URL = "http://datosabiertos.laspalmasgc.es/repositorio/policia/atestados/DB_{tipo}_{year}.csv"
YEARS = list(range(1998, 2017))

def load_csv(url, label):
    try:
        df = get_csv_df(url, encoding="latin1")
        print(f"  {label}: {len(df)} rows", flush=True)
        return df
    except Exception as e:
        print(f"  {label}: ERROR {e}", flush=True)
        return None

acc_all, her_all, veh_all = [], [], []
for y in YEARS:
    print(f"\n{y}:", flush=True)
    for tipo, alias, storage in [("ACC", "accidentes", acc_all), ("HER", "heridos", her_all), ("VEH", "vehiculos", veh_all)]:
        df = load_csv(URL.format(tipo=tipo, year=y), f"{tipo}")
        if df is not None:
            df["year"] = y
            storage.append(df)

for name, data, outfile in [
    ("Accidentes", acc_all, "atestados_acc.parquet"),
    ("Heridos", her_all, "atestados_her.parquet"),
    ("Vehiculos", veh_all, "atestados_veh.parquet"),
]:
    if data:
        combined = pd.concat(data, ignore_index=True)
        combined.to_parquet(os.path.join(OUT, outfile), index=False)
        print(f"\n{name}: {len(combined)} total rows ({len(YEARS)} years)")

print("\nDone.")
