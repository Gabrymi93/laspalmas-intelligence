# laspalmas-intelligence

Repositorio OSINT para centralizar datos HVD de **Las Palmas de Gran Canaria**.

## Fuentes

| Fuente | Tipo | Datasets | Acceso |
|--------|------|----------|--------|
| **ISTAC** (datos.canarias.es) | CKAN + REST API | ~22K datasets | CSV/TSV/JSON vía API REST |
| **Ayuntamiento LPGC** (datosabiertos.laspalmasgc.es) | WordPress/Viavansi | ~200 datasets | DCAT RDF + CKAN DataStore API |
| **SITCAN** (opendata.sitcan.es) | CKAN geo | 174 datasets | Descarga ZIP (SHP) |
| **Eurostat** | SDMX | 28 datasets NUTS-3 | MCP connector |
| **osint-canarias** (repo local) | ETL propio | Turismo elaborado | Parquet listo |

## Cobertura actual

| Dominio | Dataset | Registros | Período | Granularidad | Fuente |
|---------|---------|-----------|---------|-------------|--------|
| Población | Serie histórica | 114 | 1986-2025 | municipio | ISTAC |
| Demografía | Indicadores | 15 | 2008-2022 | municipio | ISTAC |
| Población | Por sección censal (edad, sexo, origen) | 275 | 2022 | sección | WFS ISTAC |
| Empleo | Paro por sexo/edad | 7.260 | 2008-03 → 2026-06 | municipio, mensual | ISTAC |
| Empleo | Paro por sexo/ocupación | 6.105 | 2011-02 → 2026-06 | municipio, mensual | ISTAC |
| Transporte | GTFS rutas | 47 | 2026 | línea | Ayto LPGC |
| Transporte | GTFS viajes | 6.250 | 2026 | viaje | Ayto LPGC |
| Transporte | GTFS horarios | 151.551 | 2026 | parada/viaje | Ayto LPGC |
| Transporte | GTFS calendario | 9 | 2015-2025 | servicio | Ayto LPGC |
| Transporte | Sitycleta bike stations | 11 | 2018 | estación | Ayto LPGC |
| Turismo | Ocupación hotelera | 45 | 2009-2023 | LPGC + categoría | ISTAC |
| Turismo | Pernoctaciones | 197 | 2010-2026 | Gran Canaria, mensual | ISTAC |
| Turismo | Gasto turístico | 96 | 2010-2017 | Canarias, por país | ISTAC |
| Economía | Renta bruta por municipio | 45 | 2015-2023 | LPGC por fuente | ISTAC |
| Economía | Renta bruta por sección censal | 12.395 | 2015-2023 | 281 secciones LPGC | ISTAC |
| Seguridad | Atestados accidentes | 76.178 | 1998-2016 | LPGC, calle | Ayto LPGC |
| Seguridad | Atestados heridos | 45.488 | 1998-2016 | LPGC, edad/sexo/gravedad | Ayto LPGC |
| Seguridad | Atestados vehículos | 148.650 | 1998-2016 | LPGC, marca/modelo | Ayto LPGC |
| Urbanismo | PGO Plan General | 6.608 | 2012 | polígono (ZUSO) | SITCAN |
| Urbanismo | PGO catalogación | 821 | 2012 | elemento protegido | SITCAN |
| Urbanismo | Planes parciales | 28 planes GIS | 1994-2024 | polígono (ZUSO) | SITCAN |
| Geografía | Distritos (geometría + indicadores) | 5 | 2022 | distrito | WFS ISTAC |
| Geografía | Barrios (geometría + indicadores) | 121 | 2024 | barrio | WFS ISTAC |
| Geografía | Secciones censales (geometría) | 275 | 2022 | sección | WFS ISTAC |

## Queries (35)

| # | Query | Dominio |
|---|-------|---------|
| 001 | Tendencia población LPGC 1986-2025 | Población |
| 002 | Composición por sexo | Población |
| 003 | Población extranjera | Población |
| 004 | Estructura de edad (jóvenes/adultos/mayores) | Población |
| 005 | Tendencia mensual del paro 2008-2026 | Empleo |
| 006 | Paro por sexo | Empleo |
| 007 | Paro por edad | Empleo |
| 008 | Paro anual | Empleo |
| 009 | **Patrones temporales de accidentes** (hora/día/mes/año) | Movilidad |
| 010 | Líneas de guaguas | Movilidad |
| 011 | Viajes por línea | Movilidad |
| 012 | Calendario de servicio GTFS | Movilidad |
| 013 | **Tasa de paro juvenil (16-24) por barrio** | Empleo |
| 014 | **Estructura de edad por distrito** | Demografía |
| 015 | **Renta, verde y mercado laboral por distrito** | Economía |
| 016 | **Accidentes por tipo de colisión y evolución** | Movilidad |
| 017 | **Complementariedad guaguas × Sitycleta** | Movilidad |
| 018 | **Correlación accidentes ↔ desempleo (2008-2013)** | Movilidad |
| 020 | Ocupación hotelera LPGC por categoría | Turismo |
| 021 | Pernoctaciones mensuales Gran Canaria | Turismo |
| 022 | Gasto turístico por país de origen | Turismo |
| 023 | **Estacionalidad turística (perfil mensual)** | Turismo |
| 024 | **Perfil del desempleo por grupo de edad** | Empleo |
| 025 | **Brecha de género en el desempleo** | Empleo |
| 030 | Zonificación del PGO | Urbanismo |
| 031 | Catálogo de protección | Urbanismo |
| 032 | Resumen de planeamiento | Urbanismo |
| 033 | Espacio verde pro-capite LPGC | Urbanismo |
| 034 | Renta por distrito (composición por fuente) | Economía |
| 035 | Barrios con mayor/menor tasa de paro | Geografía |
| 036 | Comparativa laboral entre distritos | Geografía |
| 037 | Espacios verdes por barrio | Urbanismo |
| 038 | Espacios verdes por distrito | Urbanismo |
| 039 | Paro vs renta por distrito | Economía |
| 040 | Evolución de la severidad de accidentes | Movilidad |

**Negrita** = queries añadidas en la sesión de julio 2026.

## Estructura

```
laspalmas-intelligence/
├── bin/                # scripts de utilidad (runner queries, status, csv2parquet)
├── ingest/             # scripts de descarga por fuente (ETL)
├── parquet/            # datos limpios en Parquet
│   ├── poblacion/      # población + indicadores + secciones
│   ├── empleo/         # paro registrado sexo/edad + sexo/ocupación
│   ├── economia/       # renta bruta por municipio y sección
│   ├── movilidad/      # GTFS + atestados policía + sitycleta
│   ├── turismo/        # ocupación, pernoctaciones, gasto
│   ├── urbanismo/      # PGO + planes parciales (GeoParquet)
│   └── geografia/      # distritos, barrios, secciones (GeoParquet + dimensión)
├── sql/                # 35 consultas DuckDB (#001-#040)
├── meta/
│   ├── catalog.json    # inventario completo de fuentes y datasets
│   └── next-session.md # plan para próxima sesión
├── explore/            # informes de análisis
├── .venv/              # entorno virtual Python
├── requirements.txt    # dependencias
├── requirements.lock   # versiones precisas
└── Makefile            # make refresh | queries | status
```

## Uso

```bash
make venv          # crear entorno virtual e instalar dependencias
make refresh       # descargar y actualizar todos los datos
make queries       # ejecutar todas las consultas (35)
make status        # resumen de datasets y filas
make all           # venv + refresh + queries + status
```

## Notas técnicas

- **DuckDB v1.5.4** via Python (package pip). El CLI `duckdb` puede estar en otra versión.
- **Spatial extension**: `ST_Transform` requiere dos SRID + `ST_FlipCoordinates` para geometrías WGS84:
  ```sql
  ST_Transform(ST_FlipCoordinates(geom), 'EPSG:4326', 'EPSG:32628')
  ```
- **Makefile** usa `$(VENV)/bin/python3` para garantizar el entorno correcto.
- Los scripts en `ingest/` son ETL independientes (cada uno descarga una fuente).
- Los scripts en `bin/` son utilidades transversales (runner, status, conversión).

## Pendiente

- **Sensores calidad del aire** (Ayto LPGC, live 2026-07, 3 recursos)
- **Callejero municipal** (base geoespacial, 15 recursos)
- **Centros educativos** (ISTAC, geolocalizados)
- **Analítica urbana** (conteo personas mercados, live)
- **Eurostat NUTS-3** (PIL, GVA, crimen ES704 como contexto provincial)
- **GTFS stops OSM** (script `fetch_gtfs_stops.py` listo, ejecutar si Overpass disponible)
- **Sitycleta Moxsi actual** (GeoJSON 2026 no descargable, solo 2018 disponible)
- **Atestados 2017+** — no publicados por el Ayuntamiento
