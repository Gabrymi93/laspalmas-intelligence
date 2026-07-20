"""
Ingest: population by seccion censal from ISTAC WFS (Padron Municipal).
Source: Indicadores demograficos. Secciones de Canarias (WFS, 2022-01-01)
Output: parquet/poblacion/poblacion_secciones.parquet
"""
import os
import urllib.request
import urllib.parse
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "poblacion")
os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/pob_secciones.csv"

WFS = "https://datos.canarias.es/api/estadisticas/geographical-resources/indicadoresdemograficos/ows"
LPGC = "35016"
LAYER = "Secciones-20220101"
YEAR = 2022

COLS = [
    "geocode", "poblacion", "poblacion_hombres", "poblacion_mujeres",
    "poblacion_edad_media", "poblacion_nacional", "poblacion_extranjera",
    "poblacion_00a14", "poblacion_15a64", "poblacion_65mas",
    "poblacion_indice_dependencia", "superficie",
    "poblacion_nacida_canarias", "poblacion_nacida_extranjero",
]

print(f"[poblacion_secciones] downloading {YEAR}...", flush=True)
cql = f"geocode LIKE '%_{LPGC}_%'"
url = (
    f"{WFS}?service=WFS&version=1.1.0&request=GetFeature"
    f"&typeName={LAYER}&outputFormat=csv"
    f"&propertyName={','.join(COLS)}"
    f"&cql_filter={urllib.parse.quote(cql)}"
)
urllib.request.urlretrieve(url, TMP)
df = pd.read_csv(TMP)
os.remove(TMP)

# Extract seccion_code: 20220101_35016_D02_S045 -> D02_S045
df["seccion_code"] = df["geocode"].str.extract(r"(D\d+_S\d+)", expand=True)[0]
df["year"] = YEAR

out_path = os.path.join(OUT, "poblacion_secciones.parquet")
df.to_parquet(out_path, index=False)
total_pop = int(df["poblacion"].sum())
print(f"  -> {len(df)} sections, total pop: {total_pop:,}")
print("Done.")
