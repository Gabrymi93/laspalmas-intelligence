"""
Ingest: población autónoma (cuenta propia) desde ISTAC.

Combina due fonti complementari:
  1. E58015B_000054 v1.76: afiliaciones por situación empleo (2010-2025, mensual)
  2. C00069A_000005 v1.12: población ocupada registrada (2011-2026, trimestral)

Output: parquet/economia/autonomos_lpgc.parquet
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import get_csv_df

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "economia")
os.makedirs(OUT, exist_ok=True)

ISTAC_API = "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC"
MUNI = "35016"


def download_csv(url, name):
    print(f"[{name}] downloading...", flush=True)
    try:
        return get_csv_df(url, dtype={"LUGAR_COTIZACION_CODE": str})
    except Exception as e:
        print(f"  x {e}")
        return None


print("\n=== Autónomos LPGC ===")

# --- 1. E58015B_000054 (2010-2025, mensual, por sector) ---
df1 = download_csv(
    f"{ISTAC_API}/E58015B_000054/1.76.csv",
    "afiliaciones_situacion_empleo"
)
if df1 is not None:
    mask = (
        (df1["LUGAR_COTIZACION_CODE"] == MUNI) &
        (df1["SITUACION_EMPLEO_CODE"] == "EMPLEOS_CUENTA_PROPIA") &
        (df1["ACTIVIDAD_ECONOMICA_CODE"] == "_T") &
        (df1["SEXO_CODE"] == "_T")
    )
    lpgc1 = df1[mask].copy()
    lpgc1 = lpgc1.rename(columns={
        "TIME_PERIOD#es": "periodo",
        "TIME_PERIOD_CODE": "periodo_code",
        "OBS_VALUE": "valor",
    })
    lpgc1["year"] = lpgc1["periodo_code"].str[:4].astype(int)
    lpgc1["valor"] = pd.to_numeric(lpgc1["valor"], errors="coerce")
    lpgc1["fuente"] = "E58015B"
    lpgc1["tipo"] = "autonomos"
    lpgc1 = lpgc1[["year", "periodo", "periodo_code", "valor", "fuente", "tipo"]]
    print(f"  E58015B: {len(lpgc1)} rows, {lpgc1['year'].min()}-{lpgc1['year'].max()}")

# --- 2. C00069A_000005 (2011-2026, trimestral) ---
df2 = download_csv(
    f"{ISTAC_API}/C00069A_000005/1.12.csv",
    "poblacion_ocupada_registrada"
)
if df2 is not None:
    mask = (
        (df2["TERRITORIO_CODE"] == MUNI) &
        (df2["SITUACION_LABORAL_REGISTRADA_CODE"] == "SELF_REG") &
        (df2["SEXO_CODE"] == "_T")
    )
    lpgc2 = df2[mask].copy()
    lpgc2 = lpgc2.rename(columns={
        "TIME_PERIOD#es": "periodo",
        "TIME_PERIOD_CODE": "periodo_code",
        "OBS_VALUE": "valor",
    })
    lpgc2["year"] = lpgc2["periodo_code"].str[:4].astype(int)
    lpgc2["valor"] = pd.to_numeric(lpgc2["valor"], errors="coerce")
    lpgc2["fuente"] = "C00069A"
    lpgc2["tipo"] = "autonomos"
    lpgc2 = lpgc2[["year", "periodo", "periodo_code", "valor", "fuente", "tipo"]]
    print(f"  C00069A: {len(lpgc2)} rows, {lpgc2['year'].min()}-{lpgc2['year'].max()}")

# --- 3. Combine ---
if df1 is not None and df2 is not None:
    # Keep E58015B for 2010-2025, C00069A for 2026
    mask1 = lpgc1["year"] <= 2025
    mask2 = lpgc2["year"] >= 2025  # small overlap for cross-check
    combined = pd.concat([lpgc1[mask1], lpgc2[mask2]], ignore_index=True)
    combined = combined.drop_duplicates(subset=["year", "periodo_code", "tipo"])
    print(f"  Combinado: {len(combined)} rows ({lpgc1['year'].min()}-{lpgc2['year'].max()})")
elif df1 is not None:
    combined = lpgc1
elif df2 is not None:
    combined = lpgc2
else:
    print("  x No data from any source")
    exit(1)

combined = combined.sort_values(["year", "periodo_code"])

out_path = os.path.join(OUT, "autonomos_lpgc.parquet")
combined.to_parquet(out_path, index=False)
print(f"\n  -> Saved: {out_path}  ({len(combined)} rows)")

# Preview
print("\n  --- Ultimos datos ---")
last = combined[combined.year == combined.year.max()]
for _, row in last.iterrows():
    if pd.notna(row["valor"]):
        print(f"    {row['periodo_code']} | {row['periodo']:35s} | {int(row['valor']):>6} autonomos")

# --- 4. Also save sector data for analysis (E58015B only) ---
if df1 is not None:
    mask_sect = (
        (df1["LUGAR_COTIZACION_CODE"] == MUNI) &
        (df1["SITUACION_EMPLEO_CODE"] == "EMPLEOS_CUENTA_PROPIA") &
        (df1["ACTIVIDAD_ECONOMICA_CODE"] != "_T") &
        (df1["SEXO_CODE"] == "_T")
    )
    sect = df1[mask_sect].copy()
    sect = sect.rename(columns={
        "TIME_PERIOD#es": "periodo",
        "TIME_PERIOD_CODE": "periodo_code",
        "ACTIVIDAD_ECONOMICA#es": "sector",
        "ACTIVIDAD_ECONOMICA_CODE": "sector_code",
        "OBS_VALUE": "valor",
    })
    sect["year"] = sect["periodo_code"].str[:4].astype(int)
    sect["valor"] = pd.to_numeric(sect["valor"], errors="coerce")
    out_sect = os.path.join(OUT, "autonomos_sectores_lpgc.parquet")
    sect.to_parquet(out_sect, index=False)
    print(f"\n  -> + sectores: {out_sect} ({len(sect)} rows, {sect['sector_code'].nunique()} sectores)")

print("\nDone.")
