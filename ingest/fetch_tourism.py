"""
Ingest: Tourism data from ISTAC for Las Palmas de Gran Canaria.

Sources:
  - Pernoctaciones por isla: ISTAC C00065A_000063 (API REST cubo estadistico)
  - Gasto turistico por pais: ISTAC C00028A_000382 (API REST cubo estadistico)
  - Ocupacion hotelera por municipio: ISTAC via CKAN (importado de osint-canarias)

Output: parquet/turismo/
"""
import os
import pandas as pd
import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "turismo")
os.makedirs(OUT, exist_ok=True)

ISTAC_API = "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0"

def download_csv(url, name):
    print(f"[{name}] Downloading...", flush=True)
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        from io import StringIO
        resp.encoding = "utf-8"  # server reports ISO-8859-1 but actual is UTF-8
        df = pd.read_csv(StringIO(resp.text))
        print(f"  -> {len(df)} rows", flush=True)
        return df
    except Exception as e:
        print(f"  ✗ {e}", flush=True)
        return None

# --- 1. Pernottamenti per isola ---
print("\n=== Pernottamenti per isola ===")
df = download_csv(
    f"{ISTAC_API}/datasets/ISTAC/C00065A_000063/1.11.csv",
    "pernottamenti"
)
if df is not None:
    df = df[df["MEDIDAS#es"] == "Pernoctaciones"].copy()
    df["anno"] = df["TIME_PERIOD_CODE"].str[:4].astype(int)
    df["mese"] = df["TIME_PERIOD_CODE"].str[5:].str.replace("M", "").astype(int)
    gc = df[df["TERRITORIO#es"] == "Gran Canaria"].groupby(
        ["anno", "mese"], as_index=False
    )["OBS_VALUE"].sum()
    gc.to_parquet(os.path.join(OUT, "pernottamenti_gran_canaria.parquet"), index=False)
    print(f"  -> Gran Canaria: {len(gc)} rows")

# --- 2. Spesa turistica per paese ---
print("\n=== Spesa turistica per paese ===")
df = download_csv(
    f"{ISTAC_API}/datasets/ISTAC/C00028A_000382/1.0.csv",
    "spesa_turistica"
)
if df is not None:
    df = df[df["MEDIDAS#es"] == "Gasto"].copy()
    df = df[df["TIME_PERIOD_CODE"].str.len() == 4].copy()
    df["anno"] = df["TIME_PERIOD_CODE"].astype(int)
    df["paese"] = df["PAIS_RESIDENCIA#es"]
    spesa = df.groupby(["anno", "paese"], as_index=False)["OBS_VALUE"].sum()
    spesa.to_parquet(os.path.join(OUT, "spesa_turistica_paesi.parquet"), index=False)
    print(f"  -> {len(spesa)} rows")

# --- 3. Occupazione hotel per categoria e municipio ---
print("\n=== Occupazione hotel LPGC ===")
df = download_csv(
    f"{ISTAC_API}/datasets/ISTAC/C00065A_000001/1.16.csv",
    "occupazione_hotel"
)
if df is not None:
    lpgc = df[df["TERRITORIO#es"] == "Las Palmas de Gran Canaria"].copy()
    lpgc = lpgc[lpgc["OBS_VALUE"].notna()].copy()
    if len(lpgc) > 0:
        lpgc["anno"] = lpgc["TIME_PERIOD_CODE"].str[:4].astype(int)
        # Annual average by category
        annuale = lpgc[lpgc["MEDIDAS#es"] == "Tasa de ocupación por habitación"].groupby(
            ["anno", "ALOJAMIENTO_TURISTICO_CATEGORIA#es"], as_index=False
        )["OBS_VALUE"].mean()
        print(f"  -> LPGC annual: {len(annuale)} rows", flush=True)
        annuale.to_parquet(os.path.join(OUT, "occupazione_hotel_lpgc.parquet"), index=False)
    else:
        print("  ✗ no LPGC data found")

print("\nDone.")
