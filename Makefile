.PHONY: all refresh population employment urbanismo tourism queries status

all: refresh queries

refresh: population employment urbanismo tourism

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

queries:
	python3 ingest/run_queries.py

status:
	@echo "=== laspalmas-intelligence ==="
	@echo "=== datasets ===" && \
	duckdb -c "SELECT 'poblacion_serie_historica' as dataset, count(*) as rows FROM read_parquet('parquet/poblacion/poblacion_serie_historica.parquet') UNION ALL SELECT 'indicadores_demograficos', count(*) FROM read_parquet('parquet/poblacion/indicadores_demograficos.parquet') UNION ALL SELECT 'paro_sexo_edad', count(*) FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet') UNION ALL SELECT 'paro_sexo_ocupacion', count(*) FROM read_parquet('parquet/empleo/paro_sexo_ocupacion.parquet') UNION ALL SELECT 'gtfs_routes', count(*) FROM read_parquet('parquet/movilidad/gtfs_routes.parquet') UNION ALL SELECT 'gtfs_trips', count(*) FROM read_parquet('parquet/movilidad/gtfs_trips.parquet') UNION ALL SELECT 'gtfs_stop_times', count(*) FROM read_parquet('parquet/movilidad/gtfs_stop_times.parquet')" && \
	echo "=== urbanismo ===" && \
	duckdb -c "SELECT 'planes_ZUSO' as layer, count(*) as archivos FROM glob('parquet/urbanismo/*_ZUSO.parquet'); SELECT 'PGO_ZUSO' as dataset, count(*) as features FROM read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet'); SELECT 'PGO_CAT' as dataset, count(*) as features FROM read_parquet('parquet/urbanismo/32ffdaab_CAT.parquet')"
