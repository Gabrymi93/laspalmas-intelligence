"""
Validate: sanity checks for all datasets.
Runs before queries to catch empty/broken data.
Exit code: 0 = ok, 1 = errors found.
"""
import os, sys
import duckdb

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = duckdb.connect()
P = lambda p: os.path.join(BASE, p)

errors = 0
checks = [
    # (path, min_rows, max_year, note)
    ("parquet/poblacion/poblacion_serie_historica.parquet", 100, 2026, "poblacion"),
    ("parquet/poblacion/indicadores_demograficos.parquet", 10, 2022, "indicadores"),
    ("parquet/poblacion/poblacion_secciones.parquet", 200, 2022, "secciones_censales"),
    ("parquet/empleo/paro_sexo_edad.parquet", 5000, 2026, "paro_registrado"),
    ("parquet/empleo/paro_sexo_ocupacion.parquet", 5000, 2026, "paro_ocupacion"),
    ("parquet/movilidad/atestados_acc.parquet", 30000, 2016, "accidentes"),
    ("parquet/movilidad/atestados_her.parquet", 20000, 2016, "heridos"),
    ("parquet/movilidad/atestados_veh.parquet", 80000, 2016, "vehiculos"),
    ("parquet/movilidad/gtfs_routes.parquet", 30, 2026, "gtfs_rutas"),
    ("parquet/movilidad/gtfs_trips.parquet", 5000, 2026, "gtfs_viajes"),
    ("parquet/movilidad/gtfs_stop_times.parquet", 100000, 2026, "gtfs_horarios"),
    ("parquet/movilidad/gtfs_stops.parquet", 500, 2026, "gtfs_paradas"),
    ("parquet/movilidad/sitycleta.parquet", 10, 2026, "sitycleta"),
    ("parquet/economia/renta_municipio_lpgc.parquet", 30, 2023, "renta_municipio"),
    ("parquet/economia/renta_secciones_lpgc.parquet", 10000, 2023, "renta_secciones"),
    ("parquet/economia/empresas_lpgc.parquet", 500, 2026, "empresas"),
    ("parquet/economia/autonomos_lpgc.parquet", 100, 2026, "autonomos"),
    ("parquet/turismo/occupazione_hotel_lpgc.parquet", 30, 2023, "turismo_hotel"),
    ("parquet/turismo/pernottamenti_gran_canaria.parquet", 100, 2026, "turismo_pernottamenti"),
    ("parquet/turismo/spesa_turistica_paesi.parquet", 50, 2017, "turismo_spesa"),
    ("parquet/geografia/callejero_lpgc.parquet", 5000, 2026, "callejero"),
    ("parquet/ambiente/calidad_aire_gemelo.parquet", 5000, 2026, "aire_gemelo"),
    ("parquet/ambiente/calidad_aire_estaciones.parquet", 50000, 2026, "aire_estaciones"),
    ("parquet/ambiente/calidad_aire_estaciones_geo.parquet", 4, 2026, "aire_estaciones_geo"),
]

print("=== Validación de datasets ===")
for path, min_rows, max_year, label in checks:
    fp = P(path)
    if not os.path.exists(fp):
        print(f"  ✗ {label}: archivo no encontrado: {path}")
        errors += 1
        continue

    try:
        row_count = con.execute(f"SELECT count(*) FROM '{fp}'").fetchone()[0]
        if row_count < min_rows:
            print(f"  ✗ {label}: {row_count} filas (mínimo {min_rows})")
            errors += 1
            continue

        # Check max year if there's a year column
        try:
            cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM '{fp}'").fetchall()]
            year_col = [c for c in cols if c.lower() in ('year', 'anno', 'año')]
            if year_col:
                max_yr = con.execute(f"SELECT max({year_col[0]}) FROM '{fp}'").fetchone()[0]
                if max_yr is None or max_yr < max_year - 2:
                    print(f"  ⚠ {label}: año máximo {max_yr} (atteso ~{max_year})")
        except:
            pass  # no year column, skip

        print(f"  ✓ {label}: {row_count} rows")

    except Exception as e:
        print(f"  ✗ {label}: error: {e}")
        errors += 1

print(f"\nResultado: {errors} errores")

# --- Check HTTP: todos los scripts de ingest deben usar http_utils ---
print("\n=== Coherencia HTTP (ingest) ===")
ingest_dir = os.path.join(BASE, "ingest")
for fn in sorted(os.listdir(ingest_dir)):
    if not fn.endswith(".py") or fn == "http_utils.py":
        continue
    fp = os.path.join(ingest_dir, fn)
    with open(fp) as f:
        src = f.read()
    # Debe importar http_utils
    if "http_utils" not in src:
        print(f"  ✗ {fn}: no importa http_utils (usa urllib/requests directo?)")
        errors += 1
        continue
    # No debe usar urllib.request.urlopen ni requests.get directamente
    if "urllib.request.urlopen" in src or "requests.get(" in src:
        print(f"  ✗ {fn}: usa urllib/requests directo en vez de http_utils")
        errors += 1
        continue
    print(f"  ✓ {fn}")

sys.exit(1 if errors else 0)
