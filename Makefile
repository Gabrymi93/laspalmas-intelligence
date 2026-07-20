.PHONY: all refresh population employment urbanismo tourism queries status

all: refresh queries

refresh: population employment urbanismo tourism renta atestados geografia poblacion_secciones

population:
	python3 ingest/istac_population.py
	python3 ingest/csv2parquet.py

employment:
	python3 ingest/istac_employment.py
	python3 ingest/csv2parquet.py

urbanismo:
	python3 ingest/fetch_urbanismo_sitcan.py

tourism:
	python3 ingest/fetch_tourism.py

renta:
	python3 ingest/istac_renta.py

atestados:
	python3 ingest/fetch_atestados.py

geografia:
	python3 ingest/fetch_geografia_wfs.py

poblacion_secciones:
	python3 ingest/fetch_poblacion_secciones.py

sitycleta:
	python3 ingest/fetch_sitycleta.py

gtfs_stops:
	python3 ingest/fetch_gtfs_stops.py

queries:
	python3 ingest/run_queries.py

status:
	@echo "=== laspalmas-intelligence ==="
	@echo "=== datasets ===" && \
	duckdb -c "SELECT 'poblacion_serie_historica' as dataset, count(*) as rows FROM read_parquet('parquet/poblacion/poblacion_serie_historica.parquet') UNION ALL SELECT 'indicadores_demograficos', count(*) FROM read_parquet('parquet/poblacion/indicadores_demograficos.parquet') UNION ALL SELECT 'poblacion_secciones', count(*) FROM read_parquet('parquet/poblacion/poblacion_secciones.parquet') UNION ALL SELECT 'paro_sexo_edad', count(*) FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet') UNION ALL SELECT 'paro_sexo_ocupacion', count(*) FROM read_parquet('parquet/empleo/paro_sexo_ocupacion.parquet') UNION ALL SELECT 'gtfs_routes', count(*) FROM read_parquet('parquet/movilidad/gtfs_routes.parquet') UNION ALL SELECT 'gtfs_trips', count(*) FROM read_parquet('parquet/movilidad/gtfs_trips.parquet') UNION ALL SELECT 'gtfs_stop_times', count(*) FROM read_parquet('parquet/movilidad/gtfs_stop_times.parquet') UNION ALL SELECT 'gtfs_stops', count(*) FROM read_parquet('parquet/movilidad/gtfs_stops.parquet') UNION ALL SELECT 'sitycleta', count(*) FROM read_parquet('parquet/movilidad/sitycleta.parquet') UNION ALL SELECT 'atestados_accidentes', count(*) FROM read_parquet('parquet/movilidad/atestados_acc.parquet') UNION ALL SELECT 'atestados_heridos', count(*) FROM read_parquet('parquet/movilidad/atestados_her.parquet') UNION ALL SELECT 'atestados_vehiculos', count(*) FROM read_parquet('parquet/movilidad/atestados_veh.parquet') UNION ALL SELECT 'renta_municipio', count(*) FROM read_parquet('parquet/economia/renta_municipio_lpgc.parquet') UNION ALL SELECT 'renta_secciones', count(*) FROM read_parquet('parquet/economia/renta_secciones_lpgc.parquet')" && \
	echo "=== urbanismo ===" && \
	duckdb -c "SELECT 'planes_ZUSO' as layer, count(*) as archivos FROM glob('parquet/urbanismo/*_ZUSO.parquet'); SELECT 'PGO_ZUSO' as dataset, count(*) as features FROM read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet'); SELECT 'PGO_CAT' as dataset, count(*) as features FROM read_parquet('parquet/urbanismo/32ffdaab_CAT.parquet'); SELECT 'distritos' as geografia, count(*) FROM read_parquet('parquet/geografia/dim_distritos.parquet'); SELECT 'barrios' as geografia, count(*) FROM read_parquet('parquet/geografia/dim_barrios.parquet'); SELECT 'secciones' as geografia, count(*) FROM read_parquet('parquet/geografia/dim_secciones.parquet')"
