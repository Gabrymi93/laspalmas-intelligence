.PHONY: all refresh population employment urbanismo tourism gtfs \
        renta atestados geografia poblacion_secciones sitycleta gtfs_stops \
        empresas autonomos callejero aire vivienda \
        queries status validate venv dashboard

VENV = .venv
PYTHON = $(VENV)/bin/python3

all: venv refresh validate queries status

$(VENV):
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip -q
	$(PYTHON) -m pip install -r requirements.txt -q

venv: $(VENV)

# ETL targets — each downloads raw data and converts to Parquet
# Failures propagate: if a dataset is broken, validate catches it
refresh: population employment urbanismo tourism gtfs renta atestados \
         geografia poblacion_secciones sitycleta gtfs_stops empresas autonomos callejero aire

population: venv
	$(PYTHON) ingest/istac_population.py
	$(PYTHON) bin/csv2parquet.py

employment: venv
	$(PYTHON) ingest/istac_employment.py
	$(PYTHON) bin/csv2parquet.py

urbanismo: venv
	$(PYTHON) ingest/fetch_urbanismo_sitcan.py

tourism: venv
	$(PYTHON) ingest/fetch_tourism.py

gtfs: venv
	$(PYTHON) ingest/fetch_gtfs.py

renta: venv
	$(PYTHON) ingest/istac_renta.py

atestados: venv
	$(PYTHON) ingest/fetch_atestados.py

geografia: venv
	$(PYTHON) ingest/fetch_geografia_wfs.py

poblacion_secciones: venv
	$(PYTHON) ingest/fetch_poblacion_secciones.py

sitycleta: venv
	$(PYTHON) ingest/fetch_sitycleta.py

gtfs_stops: venv
	$(PYTHON) ingest/fetch_gtfs_stops.py

empresas: venv
	$(PYTHON) ingest/istac_empresas.py

autonomos: venv
	$(PYTHON) ingest/istac_autonomos.py

callejero: venv
	$(PYTHON) ingest/fetch_callejero.py

aire: venv
	$(PYTHON) ingest/fetch_calidad_aire.py

vivienda: venv
	$(PYTHON) ingest/istac_vivienda_vacacional.py
	$(PYTHON) bin/csv2parquet.py

# Analysis
queries: venv
	$(PYTHON) bin/run_queries.py

validate: venv
	$(PYTHON) bin/validate.py

status: venv
	$(PYTHON) bin/run_status.py

# Dashboard
dashboard: venv
	$(PYTHON) -m streamlit run dashboard/app.py --server.port 8501 --server.headless true
