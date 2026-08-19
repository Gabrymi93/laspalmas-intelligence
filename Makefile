.PHONY: all refresh population employment urbanismo tourism gtfs \
        renta atestados geografia poblacion_secciones sitycleta gtfs_stops \
        empresas autonomos callejero aire \
        queries status validate venv

VENV = .venv
PYTHON = $(VENV)/bin/python3

all: venv refresh validate queries status

$(VENV):
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip -q
	$(PYTHON) -m pip install -r requirements.txt -q

venv: $(VENV)

# ETL targets — each downloads raw data and converts to Parquet
# Using "-k" or "|| true" so one failure doesn't block the rest
refresh: population employment urbanismo tourism gtfs renta atestados \
         geografia poblacion_secciones sitycleta gtfs_stops empresas autonomos callejero aire

population: venv
	$(PYTHON) ingest/istac_population.py && $(PYTHON) bin/csv2parquet.py || echo "⚠ population: fallo, se continua"

employment: venv
	$(PYTHON) ingest/istac_employment.py && $(PYTHON) bin/csv2parquet.py || echo "⚠ employment: fallo, se continua"

urbanismo: venv
	$(PYTHON) ingest/fetch_urbanismo_sitcan.py || echo "⚠ urbanismo: fallo, se continua"

tourism: venv
	$(PYTHON) ingest/fetch_tourism.py || echo "⚠ tourism: fallo, se continua"

gtfs: venv
	$(PYTHON) ingest/fetch_gtfs.py || echo "⚠ gtfs: fallo, se continua"

renta: venv
	$(PYTHON) ingest/istac_renta.py || echo "⚠ renta: fallo, se continua"

atestados: venv
	$(PYTHON) ingest/fetch_atestados.py || echo "⚠ atestados: fallo, se continua"

geografia: venv
	$(PYTHON) ingest/fetch_geografia_wfs.py || echo "⚠ geografia: fallo, se continua"

poblacion_secciones: venv
	$(PYTHON) ingest/fetch_poblacion_secciones.py || echo "⚠ poblacion_secciones: fallo, se continua"

sitycleta: venv
	$(PYTHON) ingest/fetch_sitycleta.py || echo "⚠ sitycleta: fallo, se continua"

gtfs_stops: venv
	$(PYTHON) ingest/fetch_gtfs_stops.py || echo "⚠ gtfs_stops: fallo, se continua"

empresas: venv
	$(PYTHON) ingest/istac_empresas.py || echo "⚠ empresas: fallo, se continua"

autonomos: venv
	$(PYTHON) ingest/istac_autonomos.py || echo "⚠ autonomos: fallo, se continua"

callejero: venv
	$(PYTHON) ingest/fetch_callejero.py || echo "⚠ callejero: fallo, se continua"

aire: venv
	$(PYTHON) ingest/fetch_calidad_aire.py || echo "⚠ aire: fallo, se continua"

# Analysis
queries: venv
	$(PYTHON) bin/run_queries.py

validate: venv
	$(PYTHON) bin/validate.py

status: venv
	$(PYTHON) bin/run_status.py
