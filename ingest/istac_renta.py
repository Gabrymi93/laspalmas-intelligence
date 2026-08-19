"""
Ingest: income distribution (renta bruta media) from ISTAC.
Sources:
  - E30325A_000002: by municipality, 2015-2023
  - E30325A_000014..000055: by seccion censal, 2015-2023 (one cube per year)
Output: parquet/economia/
"""
import os
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import get_csv_df

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "economia")
os.makedirs(OUT, exist_ok=True)

ISTAC_API = "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC"
MUNI_CODE = "35016"
CODIGOS_PROVINCIA = {"ES70", "ES701", "ES702", "ES703", "ES704", "ES705", "ES706", "ES707", "ES708", "ES709"}

SECCION_CUBES = {
    2015: ("E30325A_000014", "1.1"),
    2016: ("E30325A_000015", "1.1"),
    2017: ("E30325A_000016", "1.1"),
    2018: ("E30325A_000017", "1.1"),
    2019: ("E30325A_000018", "1.1"),
    2020: ("E30325A_000040", "1.1"),
    2021: ("E30325A_000045", "1.1"),
    2022: ("E30325A_000050", "1.1"),
    2023: ("E30325A_000055", "1.0"),
}

def download_csv(url, name):
    print(f"[{name}] downloading...", flush=True)
    try:
        return get_csv_df(url)
    except Exception as e:
        print(f"  x {e}")
        return None

# --- 1. Municipality-level: all years ---
print("\n=== Renta bruta por municipio (2015-2023) ===")
df = download_csv(
    f"{ISTAC_API}/E30325A_000002/2.3.csv",
    "renta_municipio"
)
if df is not None:
    df["year"] = df["TIME_PERIOD_CODE"].astype(int)
    lpgc = df[df["TERRITORIO_CODE"] == MUNI_CODE].copy()
    lpgc = lpgc.rename(columns={"MEDIDAS#es": "medida", "MEDIDAS_CODE": "medida_code", "OBS_VALUE": "valor"})
    lpgc.to_parquet(os.path.join(OUT, "renta_municipio_lpgc.parquet"), index=False)
    print(f"  -> LPGC (municipio): {len(lpgc)} rows ({lpgc['year'].nunique()} years)")


# --- 2. Section-level: one cube per year ---
print("\n=== Renta bruta por seccion censal (2015-2023) ===")
all_sections = []
for year, (cube, ver) in sorted(SECCION_CUBES.items()):
    name = f"renta_seccion_{year}"
    df = download_csv(f"{ISTAC_API}/{cube}/{ver}.csv", name)
    if df is not None and len(df) > 0:
        mask = df["TERRITORIO_CODE"].str.contains(f"_{MUNI_CODE}_", na=False)
        lpgc = df[mask].copy()
        if len(lpgc) > 0:
            lpgc["year"] = year
            lpgc["seccion_code"] = lpgc["TERRITORIO_CODE"].str.extract(r"D(\d+)_S(\d+)", expand=True).apply(
                lambda r: f"D{int(r[0]):02d}_S{int(r[1]):03d}" if pd.notna(r[0]) else None, axis=1
            )
            all_sections.append(lpgc)
            print(f"  -> {year}: {len(lpgc)} rows")
        else:
            print(f"  -> {year}: 0 LPGC sections")
    else:
        print(f"  -> {year}: no data")

if all_sections:
    combined = pd.concat(all_sections, ignore_index=True)
    combined = combined.rename(columns={
        "MEDIDAS#es": "medida", "MEDIDAS_CODE": "medida_code", "OBS_VALUE": "valor"
    })
    out_path = os.path.join(OUT, "renta_secciones_lpgc.parquet")
    combined.to_parquet(out_path, index=False)
    print(f"\n  -> Total LPGC sections: {combined['seccion_code'].nunique()} sections, {len(combined)} rows")

print("\nDone.")
