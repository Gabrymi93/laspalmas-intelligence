"""
Ingest: Sensores de calidad del aire (proyecto Gemelo Digital).
Source: CKAN DataStore Ayuntamiento LPGC + ArcGIS FeatureServer
Dataset CKAN: sensores-de-calidad-del-aire (940cc41a-4e25-4c3d-8d96-ad1047420919)
Output:
  parquet/ambiente/calidad_aire_gemelo.parquet        (sensores propios, ~7.7k lecturas)
  parquet/ambiente/calidad_aire_estaciones.parquet    (estaciones Gob. de Canarias, ~118k lecturas)
  parquet/ambiente/calidad_aire_estaciones_geo.parquet (ubicación de las estaciones)
"""
import os
import json
import urllib.parse
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from http_utils import fetch_json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "ambiente")
os.makedirs(OUT, exist_ok=True)

SQL = "http://apidatosabiertos.laspalmasgc.es/api/3/action/datastore_search_sql"
R1 = "4f653821-b6c8-483a-b9a4-b919ac41f4ac"  # Sensores propios de Gemelo Digital
R2 = "1ce26979-183e-4dc3-98e7-739628e8c554"  # Sensores del Gobierno de Canarias

PAGE = 10000

def fetch_datastore(resource_id):
    # NOTA: datastore_search con paginación offset es inestable (devuelve duplicados).
    # Se usa datastore_search_sql con ORDER BY _id (paginación determinista).
    records = []
    offset = 0
    while True:
        q = f'SELECT * FROM "{resource_id}" ORDER BY "_id" LIMIT {PAGE} OFFSET {offset}'
        url = f"{SQL}?{urllib.parse.urlencode({'sql': q})}"
        data = fetch_json(url)
        if not data.get("success"):
            raise RuntimeError(f"datastore_search_sql error: {data.get('error')}")
        page = data["result"].get("records", [])
        records.extend(page)
        offset += PAGE
        if len(page) < PAGE:
            break
        print(f"  Descargadas: {len(records)}", end="\r")
    return records


def save(df, name):
    path = os.path.join(OUT, name)
    df.to_parquet(path, index=False)
    print(f"  -> Saved: {path} ({len(df)} rows)")


# --- R1: Sensores propios de Gemelo Digital ---
print("\n=== Calidad del aire: sensores propios (Gemelo Digital) ===")
recs1 = fetch_datastore(R1)
if not recs1:
    print("  x No data from R1")
    exit(1)
df1 = pd.DataFrame(recs1)
df1 = df1.rename(columns={
    "PM2_5": "pm2_5", "PM_10": "pm_10", "iaqIndex": "iaq_index",
    "icIndex": "ic_index", "idaIndex": "ida_index",
    "indiceCalidadSeñalNum": "indice_calidad_senal", "ObjectId": "objectid",
    "datetimepretty": "datetime",
})
df1 = df1.drop(columns=["_full_text"], errors="ignore")
df1["date"] = pd.to_numeric(df1["date"], errors="coerce").astype("Int64")
df1["datetime"] = pd.to_datetime(df1["datetime"], errors="coerce")
save(df1, "calidad_aire_gemelo.parquet")
print(f"  Mercados: {df1['mercado'].value_counts().to_dict()}")
print(f"  Sensores: {sorted(df1['label'].unique())}")
print(f"  Período: {df1['datetime'].min()} -> {df1['datetime'].max()}")

# --- R2: Sensores del Gobierno de Canarias (formato largo por parámetro) ---
print("\n=== Calidad del aire: estaciones Gobierno de Canarias ===")
recs2 = fetch_datastore(R2)
if not recs2:
    print("  x No data from R2")
    exit(1)
df2 = pd.DataFrame(recs2)
df2 = df2.rename(columns={
    "_id": "id", "OBJECTID": "objectid", "nombreEstacion": "nombre_estacion",
    "nombreParametro": "nombre_parametro", "valorTexto": "valor_texto",
    "valorNumerico": "valor_numerico", "Fecha": "fecha",
    "datetimepretty": "datetime",
})
df2 = df2.drop(columns=["_full_text"], errors="ignore")
df2["datetime"] = pd.to_datetime(df2["datetime"], errors="coerce")
save(df2, "calidad_aire_estaciones.parquet")
print(f"  Estaciones: {sorted(df2['nombre_estacion'].unique())}")
print(f"  Parámetros: {sorted(df2['nombre_parametro'].unique())}")
print(f"  Período: {df2['datetime'].min()} -> {df2['datetime'].max()}")

# --- Ubicaciones de las estaciones (ArcGIS FeatureServer) ---
print("\n=== Ubicación de las estaciones (FeatureServer) ===")
FS_QUERY = ("https://services-eu1.arcgis.com/eV9RayDSwR2BokOl/ArcGIS/rest/services/"
            "EstacionesCalidadAire/FeatureServer/0/query")
params = urllib.parse.urlencode({"where": "1=1", "outFields": "*",
                                 "returnGeometry": "true", "f": "geojson"})
geojson = fetch_json(f"{FS_QUERY}?{params}", timeout=60)

rows = []
for f in geojson.get("features", []):
    props = f.get("properties", {})
    lon, lat = f.get("geometry", {}).get("coordinates", [None, None])
    rows.append({"objectid": props.get("OBJECTID"), "nombre": props.get("Nombre"),
                 "lat": lat, "lon": lon})
dfg = pd.DataFrame(rows)
save(dfg, "calidad_aire_estaciones_geo.parquet")
print(f"  Estaciones: {sorted(dfg['nombre'].tolist())}")

print("\nDone.")
