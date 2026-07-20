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
| Turismo | Ocupación hotelera | 144 | 2009-2026 | LPGC + categoría | ISTAC |
| Turismo | Pernoctaciones | 197 | 2010-2026 | Gran Canaria, mensual | ISTAC |
| Turismo | Gasto turístico | 96 | 2010-2017 | Canarias, por país | ISTAC |
| Economía | Renta bruta por municipio | 45 | 2015-2023 | LPGC por fuente | ISTAC |
| Economía | Renta bruta por sección censal | 12.395 | 2015-2023 | 281 secciones LPGC | ISTAC |
| Seguridad | Atestados accidentes | 76.178 | 1998-2016 | LPGC, calle | Ayto LPGC |
| Seguridad | Atestados heridos | 45.488 | 1998-2016 | LPGC, edad/sexo/gravedad | Ayto LPGC |
| Seguridad | Atestados vehículos | 148.650 | 1998-2016 | LPGC, marca/modelo | Ayto LPGC |
| Urbanismo | PGO Plan General | 6.608 | 2012 | poligono (ZUSO) | SITCAN |
| Urbanismo | PGO catalogación | 821 | 2012 | elemento protegido | SITCAN |
| Urbanismo | Planes parciales | 28 planes GIS | 1994-2024 | poligono (ZUSO) | SITCAN |
| Geografía | Distritos (geometría + indicadores) | 5 | 2022 | distrito | WFS ISTAC |
| Geografía | Barrios (geometría + indicadores) | 121 | 2024 | barrio | WFS ISTAC |
| Geografía | Secciones censales (geometría) | 275 | 2022 | sección | WFS ISTAC |

## Estructura

```
laspalmas-intelligence/
├── ingest/              # scripts de descarga por fuente
│   ├── istac_population.py         # población histórica
│   ├── istac_employment.py         # paro registrado
│   ├── istac_renta.py              # renta bruta por sección
│   ├── fetch_gtfs.py               # GTFS Guaguas Municipales
│   ├── fetch_gtfs_stops.py         # coordenadas paradas (OSM)
│   ├── fetch_atestados.py          # accidentes policía local
│   ├── fetch_tourism.py            # turismo ISTAC
│   ├── fetch_urbanismo_sitcan.py   # planeamiento SITCAN
│   ├── fetch_geografia_wfs.py      # distritos/barrios/secciones
│   ├── fetch_poblacion_secciones.py # población por sección
│   ├── fetch_sitycleta.py          # bike sharing
│   └── run_queries.py
├── parquet/             # datos limpios en Parquet
│   ├── poblacion/       # población + indicadores
│   ├── empleo/          # paro registrado
│   ├── economia/        # renta bruta por municipio y sección
│   ├── movilidad/       # GTFS + atestados policía
│   ├── turismo/         # ocupación, pernoctaciones, gasto
│   ├── urbanismo/       # PGO + planes parciales (73 GeoParquet)
│   └── geografia/       # distritos, barrios, secciones (GeoParquet + dims)
├── sql/                 # 25 consultas DuckDB (#001-#040)
├── meta/
│   ├── catalog.json     # inventario completo de fuentes y datasets
│   └── next-session.md  # plan para próxima sesión
└── Makefile             # make refresh | queries | status
```

## Uso

```bash
make refresh   # descarga y actualiza todos los datos
make queries   # ejecuta todas las consultas
make status    # resumen de datasets y filas
```

## Pendiente

- **Sensores calidad del aire** (Ayto LPGC, live 2026-07, 3 recursos)
- **Callejero municipal** (base geoespacial, 15 recursos)
- **Eurostat NUTS-3** (PIL, GVA, crimen ES704 como contexto provincial)
- **Centros educativos** (ISTAC, geolocalizados)
- **Analítica urbana** (conteo personas mercados, live)
- **GTFS stops OSM** (script `fetch_gtfs_stops.py` listo, ejecutar si Overpass disponible)
- **Sitycleta Moxsi actual** (GeoJSON 2026 no descargable, solo 2018 disponible)
- **Atestados 2017+** — non pubblicati dal Ayuntamiento
