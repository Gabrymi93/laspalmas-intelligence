"""Status: row counts for all datasets."""
import duckdb, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = duckdb.connect()
P = lambda p: os.path.join(BASE, p)

datasets = [
    ("poblacion_serie_historica", "parquet/poblacion/poblacion_serie_historica.parquet"),
    ("indicadores_demograficos", "parquet/poblacion/indicadores_demograficos.parquet"),
    ("poblacion_secciones", "parquet/poblacion/poblacion_secciones.parquet"),
    ("paro_sexo_edad", "parquet/empleo/paro_sexo_edad.parquet"),
    ("paro_sexo_ocupacion", "parquet/empleo/paro_sexo_ocupacion.parquet"),
    ("gtfs_routes", "parquet/movilidad/gtfs_routes.parquet"),
    ("gtfs_trips", "parquet/movilidad/gtfs_trips.parquet"),
    ("gtfs_stop_times", "parquet/movilidad/gtfs_stop_times.parquet"),
    ("gtfs_stops", "parquet/movilidad/gtfs_stops.parquet"),
    ("sitycleta", "parquet/movilidad/sitycleta.parquet"),
    ("atestados_accidentes", "parquet/movilidad/atestados_acc.parquet"),
    ("atestados_heridos", "parquet/movilidad/atestados_her.parquet"),
    ("atestados_vehiculos", "parquet/movilidad/atestados_veh.parquet"),
    ("renta_municipio", "parquet/economia/renta_municipio_lpgc.parquet"),
    ("renta_secciones", "parquet/economia/renta_secciones_lpgc.parquet"),
    ("turismo_occupazione", "parquet/turismo/occupazione_hotel_lpgc.parquet"),
    ("turismo_pernottamenti", "parquet/turismo/pernottamenti_gran_canaria.parquet"),
    ("turismo_spesa", "parquet/turismo/spesa_turistica_paesi.parquet"),
    ("geografia_barrios", "parquet/geografia/barrios_lpgc.parquet"),
    ("geografia_distritos", "parquet/geografia/distritos_lpgc.parquet"),
    ("geografia_hierarchy", "parquet/geografia/dim_hierarchy.parquet"),
    ("urbanismo_ZUSO", "parquet/urbanismo/32ffdaab_ZUSO.parquet"),
    ("empresas_lpgc", "parquet/economia/empresas_lpgc.parquet"),
    ("autonomos_lpgc", "parquet/economia/autonomos_lpgc.parquet"),
    ("callejero_lpgc", "parquet/geografia/callejero_lpgc.parquet"),
    ("calidad_aire_gemelo", "parquet/ambiente/calidad_aire_gemelo.parquet"),
    ("calidad_aire_estaciones", "parquet/ambiente/calidad_aire_estaciones.parquet"),
    ("calidad_aire_estaciones_geo", "parquet/ambiente/calidad_aire_estaciones_geo.parquet"),
]

print("=== datasets ===")
print(f"{'dataset':<30} {'rows':>10}")
print("-" * 42)
for name, path in datasets:
    fp = P(path)
    if os.path.exists(fp):
        rows = con.execute(f"SELECT count(*) FROM '{fp}'").fetchone()[0]
        print(f"{name:<30} {rows:>10}")
    else:
        print(f"{name:<30} {'N/A':>10}")

print()
print("=== urbanismo ===")
zuso = con.sql("SELECT count(*) FROM glob('" + P("parquet/urbanismo/*_ZUSO.parquet") + "')").fetchone()[0]
pgo_z = con.sql("SELECT count(*) FROM '" + P("parquet/urbanismo/32ffdaab_ZUSO.parquet") + "'").fetchone()[0]
pgo_c = con.sql("SELECT count(*) FROM '" + P("parquet/urbanismo/32ffdaab_CAT.parquet") + "'").fetchone()[0]
print(f"{'planes_ZUSO':<30} {zuso:>10}")
print(f"{'PGO_ZUSO':<30} {pgo_z:>10}")
print(f"{'PGO_CAT':<30} {pgo_c:>10}")

print()
print("=== geografia ===")
for name, path in [("distritos", "parquet/geografia/dim_distritos.parquet"),
                    ("barrios", "parquet/geografia/dim_barrios.parquet"),
                    ("secciones", "parquet/geografia/dim_secciones.parquet")]:
    fp = P(path)
    if os.path.exists(fp):
        rows = con.execute(f"SELECT count(*) FROM '{fp}'").fetchone()[0]
        print(f"{name:<30} {rows:>10}")
