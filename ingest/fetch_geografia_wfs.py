"""
Ingest: geographic dimension from ISTAC WFS (Barrios, Distritos, Secciones).
Builds a geographic hierarchy for Las Palmas de Gran Canaria.
Output: parquet/geografia/ (GeoParquet + dimension table)
"""
import json
import os
import urllib.request
import duckdb

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "parquet", "geografia")
os.makedirs(OUT, exist_ok=True)

WFS = "https://datos.canarias.es/api/estadisticas/geographical-resources/epareg/ows"
LPGC = "35016"

def wfs_request(type_name, cql_filter=None, max_features=2000):
    params = [
        "service=WFS",
        "version=1.1.0",
        "request=GetFeature",
        f"typeName={type_name}",
        "outputFormat=application/json",
    ]
    if cql_filter:
        params.append(f"cql_filter={urllib.request.quote(cql_filter)}")
    params.append(f"maxFeatures={max_features}")
    url = f"{WFS}?{'&'.join(params)}"
    print(f"  {url[:120]}...", flush=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def save_geoparquet(features, out_path, layer_name):
    if not features:
        print(f"  -> 0 features, skipping")
        return
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    # Build NDJSON with geometry
    rows = []
    for f in features:
        props = f["properties"]
        geom = f.get("geometry")
        if geom is None:
            continue
        flat = {k: v for k, v in props.items() if v is not None}
        flat["geom"] = json.dumps(geom)
        rows.append(flat)

    if not rows:
        print(f"  -> no valid geometries")
        con.close()
        return

    import pandas as pd
    df = pd.DataFrame(rows)
    # Register in DuckDB and convert geom to spatial type
    con.register("tmp", df)
    con.execute(f"""
        CREATE TABLE geo AS
        SELECT *, ST_GeomFromGeoJSON(geom) as geometry
        FROM tmp
    """)
    con.execute(f"COPY (SELECT * EXCLUDE(geom) FROM geo) TO '{out_path}' (FORMAT PARQUET)")
    count = con.execute(f"SELECT count(*) FROM '{out_path}'").fetchone()[0]
    print(f"  -> {count} features saved")
    con.close()

# --- Distritos-2022 ---
print("\n=== Distritos 2022 ===")
data = wfs_request("epareg:Distritos-2022", f"geocode LIKE '%_{LPGC}_%'")
save_geoparquet(data.get("features", []), os.path.join(OUT, "distritos_lpgc.parquet"), "distritos")
# Also save dimension table (no geometry)
dist_feats = data.get("features", [])
if dist_feats:
    import pandas as pd
    dist_rows = []
    for f in dist_feats:
        p = f["properties"]
        gc = p.get("geocode", "")
        if gc and gc.split("_")[1] == LPGC:
            # Extract distrito code: 20220101_35016_D01 -> D01
            dcode = gc.split("_")[2] if len(gc.split("_")) > 2 else ""
            dist_rows.append({"geocode": gc, "distrito_code": dcode, "label": p.get("label"),
                              "pact_t": p.get("pact_t"), "pocu_t": p.get("pocu_t"),
                              "ppar_t": p.get("ppar_t"), "tpar_t": p.get("tpar_t"),
                              "psal_t": p.get("psal_t"), "tsal_t": p.get("tsal_t")})
    df = pd.DataFrame(dist_rows)
    df.to_parquet(os.path.join(OUT, "dim_distritos.parquet"), index=False)
    print(f"  -> dim_distritos: {len(df)} rows")

# --- Barrios-2024 ---
print("\n=== Barrios 2024 ===")
data = wfs_request("epareg:Barrios-2024", f"geocode LIKE '2024_{LPGC}%'")
save_geoparquet(data.get("features", []), os.path.join(OUT, "barrios_lpgc.parquet"), "barrios")
bar_feats = data.get("features", [])
if bar_feats:
    import pandas as pd
    bar_rows = []
    for f in bar_feats:
        p = f["properties"]
        gc = p.get("geocode", "")
        if gc and gc.split("_")[1] == LPGC:
            # geocode: 2024_35016_NOMBRE
            bar_rows.append({"geocode": gc, "barrio_slug": gc.split("_", 2)[2] if len(gc.split("_")) > 2 else "",
                             "label": p.get("label"),
                             "pact_t": p.get("pact_t"), "pocu_t": p.get("pocu_t"),
                             "ppar_t": p.get("ppar_t"), "tpar_t": p.get("tpar_t")})
    df = pd.DataFrame(bar_rows)
    df.to_parquet(os.path.join(OUT, "dim_barrios.parquet"), index=False)
    print(f"  -> dim_barrios: {len(df)} rows")

# --- Secciones-2022 ---
print("\n=== Secciones 2022 ===")
data = wfs_request("epareg:Secciones-2022", f"geocode LIKE '%_{LPGC}_%'")
save_geoparquet(data.get("features", []), os.path.join(OUT, "secciones_lpgc.parquet"), "secciones")
sec_feats = data.get("features", [])
if sec_feats:
    import pandas as pd
    sec_rows = []
    for f in sec_feats:
        p = f["properties"]
        gc = p.get("geocode", "")
        parts = gc.split("_")
        if len(parts) >= 4 and parts[1] == LPGC:
            dcode = parts[2]  # D01
            scode_full = f"{parts[2]}_{parts[3]}"  # D01_S021
            sec_rows.append({"geocode": gc, "distrito_code": dcode, "seccion_code": scode_full,
                             "label": p.get("label")})
    df = pd.DataFrame(sec_rows)
    df.to_parquet(os.path.join(OUT, "dim_secciones.parquet"), index=False)
    print(f"  -> dim_secciones: {len(df)} rows")

# --- Build dimension hierarchy ---
print("\n=== Dimension hierarchy ===")
con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute("""
    CREATE TABLE hier AS
    SELECT s.geocode as seccion_geocode,
           s.distrito_code,
           s.seccion_code,
           d.label as distrito_label,
           d.pact_t as distrito_pact_t,
           d.tpar_t as distrito_tpar_t
    FROM read_parquet('parquet/geografia/dim_secciones.parquet') s
    LEFT JOIN read_parquet('parquet/geografia/dim_distritos.parquet') d
      ON s.distrito_code = d.distrito_code
""")
con.execute("COPY hier TO 'parquet/geografia/dim_hierarchy.parquet' (FORMAT PARQUET)")
cnt = con.execute("SELECT count(*) FROM hier").fetchone()[0]
con.close()
print(f"  -> dim_hierarchy: {cnt} rows")

print("\nDone.")
