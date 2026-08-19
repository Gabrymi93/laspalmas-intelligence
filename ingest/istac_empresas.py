"""
Ingest: empresas por estrato de asalariados desde ISTAC.

Source: ISTAC:E58028A_000005 v2.62 (actualizado 2026-07-14)
  - Empresas inscritas en la Seguridad Social por intervalo de asalariados
  - Municipios de Canarias, 2012-2026 (mensual desde 2020, trimestral antes)
  - Categorías: Total, 1-9, 10-49, 50-249, 250+ asalariados

Output: parquet/economia/empresas_lpgc.parquet
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import get_csv_df

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "economia")
os.makedirs(OUT, exist_ok=True)

CSV_URL = ("https://datos.canarias.es/api/estadisticas/statistical-resources/"
           "v1.0/datasets/ISTAC/E58028A_000005/2.62.csv")

print("\n=== Empresas por estrato de asalariados (2012-2026) ===")
print("Downloading...", flush=True)

try:
    df = get_csv_df(CSV_URL)
except Exception as e:
    print(f"  x Download failed: {e}")
    exit(1)

print(f"  Total rows: {len(df)}")

# Filter for LPGC municipality (codigo 35016)
lpgc = df[df["TERRITORIO_CODE"] == "35016"].copy()
print(f"  LPGC rows: {len(lpgc)}")

# Standardize column names
lpgc = lpgc.rename(columns={
    "TIME_PERIOD#es": "periodo",
    "TIME_PERIOD_CODE": "periodo_code",
    "TERRITORIO#es": "territorio",
    "TERRITORIO_CODE": "territorio_code",
    "INTERVALOS_ASALARIADOS#es": "estrato",
    "INTERVALOS_ASALARIADOS_CODE": "estrato_code",
    "MEDIDAS#es": "medida",
    "MEDIDAS_CODE": "medida_code",
    "OBS_VALUE": "valor",
})

# Parse year
lpgc["year"] = lpgc["periodo_code"].str[:4].astype(int)
lpgc["valor"] = pd.to_numeric(lpgc["valor"], errors="coerce")

# Add estrato labels
estrato_label_map = {
    "_T": "Total",
    "1T9": "1-9 asalariados",
    "10T49": "10-49 asalariados",
    "50T249": "50-249 asalariados",
    "GE250": "250+ asalariados",
}
lpgc["estrato_label"] = lpgc["estrato_code"].map(estrato_label_map)

print(f"  Anios: {lpgc['year'].min()} - {lpgc['year'].max()}")
print(f"  Estratos: {sorted(lpgc['estrato_code'].unique())}")
print(f"  Periodos: {lpgc['periodo_code'].nunique()}")
print(f"  Mensual desde: {lpgc[lpgc.periodo_code.str.contains('M')]['periodo_code'].min()}")

out_path = os.path.join(OUT, "empresas_lpgc.parquet")
lpgc.to_parquet(out_path, index=False)
print(f"\n  -> Saved: {out_path} ({len(lpgc)} rows)")

# Preview latest data
print("\n  --- Ultimos datos (2026) ---")
last = lpgc[(lpgc.year == lpgc.year.max()) & lpgc.periodo_code.str.contains("M")]
for estrato in ["_T", "1T9", "10T49", "50T249", "GE250"]:
    row = last[last.estrato_code == estrato].head(1)
    if len(row) > 0:
        v = int(row.iloc[0]["valor"])
        p = int(row.iloc[0]["periodo_code"][-2:])
        print(f"    {row.iloc[0]['periodo_code']}: {row.iloc[0]['estrato_label']:20s} = {v:>6}")

print("\nDone.")
