# laspalmas-intelligence

[![ci](https://github.com/Gabrymi93/laspalmas-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Gabrymi93/laspalmas-intelligence/actions/workflows/ci.yml)
[![refresh](https://github.com/Gabrymi93/laspalmas-intelligence/actions/workflows/refresh.yml/badge.svg)](https://github.com/Gabrymi93/laspalmas-intelligence/actions/workflows/refresh.yml)

Repositorio OSINT para centralizar datos HVD de **Las Palmas de Gran Canaria**.

## Uso rápido

```bash
make venv          # entorno virtual
make refresh       # descargar datos
make validate      # validar integridad
make queries       # ejecutar 44 consultas
make status        # resumen de datasets
make all           # todo lo anterior
make dashboard     # lanzar dashboard Streamlit
```

## Dashboard Streamlit

Dashboard interactiva con 8 páginas que exploran los datos de LPGC:

| Página | Contenido |
|--------|-----------|
| 🏙️ Resumen | KPIs generales, tendencia población, paro por sexo/distrito |
| 👥 Demografía | Estructura de edad, envejecimiento, secciones censales |
| 💼 Empleo | Paro por sexo/edad/barrio, brecha de género, paro juvenil |
| 💰 Economía | Renta por distrito, empresas, autónomos, demanda coworking |
| 🏨 Turismo | Ocupación hotelera, pernotaciones, gasto por país |
| 🚌 Movilidad | Accidentes de tráfico, GTFS, Sitycleta |
| 🌬️ Ambiente | Calidad del aire, estaciones, sensores Gemelo Digital |
| 🗺️ Geografía | Mapa choropleth distritos, comparativa, callejero |

```bash
make dashboard     # o: .venv/bin/streamlit run dashboard/app.py
```

**Stack**: Streamlit + Plotly + Folium + DuckDB (lee Parquet directamente).

## Documentación

| Documento | Contenido |
|-----------|----------|
| [docs/sources.md](docs/sources.md) | Fuentes, endpoints API, scripts de ingest |
| [docs/datasets.md](docs/datasets.md) | Cobertura, granularidad, períodos |
| [docs/queries.md](docs/queries.md) | Catálogo completo de las 41 consultas SQL |
| [docs/architecture.md](docs/architecture.md) | Estructura del repo, Makefile, CI/CD |
| [meta/catalog.json](meta/catalog.json) | Inventario machine-readable de fuentes y datasets |
| [explore/analisis-resultados.md](explore/analisis-resultados.md) | Informes de análisis exploratorio |

## Notas técnicas

- DuckDB **v1.5.4** via Python (`.venv/bin/python3`). El CLI del sistema puede estar en otra versión.
- Los scripts en `bin/` son utilidades; los de `ingest/` son ETL independientes.
- `make queries` usa DuckDB v1.5.4 (no el CLI).

## Aviso legal

- Todos los datos provienen de **fuentes públicas oficiales** (ISTAC, Ayuntamiento de Las Palmas de Gran Canaria, SITCAN, Eurostat).
- Este repositorio no modifica los datos originales; solo los transforma a Parquet.
- Los datos se proporcionan **"tal cual"** (`as is`). Verifique con la fuente oficial para usos críticos.
- Código distribuido bajo licencia **MIT** (ver `LICENSE`).

## Pendiente

- Centros educativos (ISTAC, geolocalizados)
- Analítica urbana (conteo mercados)
- Eurostat NUTS-3 contexto provincial (ES704)
