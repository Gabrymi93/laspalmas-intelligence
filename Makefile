.PHONY: all refresh population employment urbanismo tourism gtfs queries status

all: refresh queries

refresh: population employment urbanismo tourism gtfs renta atestados geografia poblacion_secciones

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

gtfs:
	python3 ingest/fetch_gtfs.py

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
	python3 ingest/run_status.py
