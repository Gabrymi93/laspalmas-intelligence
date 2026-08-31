FROM python:3.12-slim

WORKDIR /app

# System deps for DuckDB spatial
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev gdal-bin libproj-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# DuckDB spatial extension (install once at build time)
RUN python -c "import duckdb; c=duckdb.connect(); c.execute('INSTALL spatial')"

# App code
COPY dashboard/ ./dashboard/
COPY parquet/ ./parquet/
COPY sql/ ./sql/
COPY meta/ ./meta/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "dashboard/app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
