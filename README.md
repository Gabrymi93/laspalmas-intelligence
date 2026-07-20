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
| Empleo | Paro por sexo/edad | 7.260 | 2008-03 → 2026-06 | municipio, mensual | ISTAC |
| Empleo | Paro por sexo/ocupación | 6.105 | 2011-02 → 2026-06 | municipio, mensual | ISTAC |
| Transporte | GTFS rutas | 47 | 2026 | línea | Ayto LPGC |
| Transporte | GTFS viajes | 6.250 | 2026 | viaje | Ayto LPGC |
| Transporte | GTFS horarios | 151.551 | 2026 | parada/viaje | Ayto LPGC |
| Transporte | GTFS calendario | 9 | 2015-2025 | servicio | Ayto LPGC |
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
| Geografía | Distritos (geometría + datos) | 5 | 2022 | distrito | WFS ISTAC |
| Geografía | Barrios (geometría + datos) | 121 | 2024 | barrio | WFS ISTAC |
| Geografía | Secciones censales (geometría) | 275 | 2022 | sección | WFS ISTAC |

## Estructura

```
laspalmas-intelligence/
├── ingest/              # scripts de descarga por fuente
│   ├── istac_population.py
│   ├── istac_employment.py
│   ├── fetch_gtfs.py
│   ├── fetch_urbanismo_sitcan.py
│   ├── csv2parquet.py
│   └── run_queries.py
├── parquet/             # datos limpios en Parquet
│   ├── poblacion/       # población + indicadores
│   ├── empleo/          # paro registrado
│   ├── economia/        # renta bruta por municipio y sección
│   ├── movilidad/       # GTFS + atestados policía
│   ├── turismo/         # ocupación, pernoctaciones, gasto
│   ├── urbanismo/       # PGO + planes parciales (73 GeoParquet)
│   └── geografia/       # distritos, barrios, secciones (GeoParquet + dims)
├── sql/                 # 18 consultas DuckDB (#001-#033)
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

## Pendiente para próxima sesión

- **Población por barrio/distrito** — ora abbiamo pact_t (población activa) da WFS come proxy. Manca población total por barrio.
- **Sensores calidad del aire** (Ayto LPGC, tiempo real 2026-07)
- **Stops GTFS** (coordenadas de paradas — 403 bloqueado, alternativa OSM o scraping)
- **Eurostat NUTS-3** (PIL, GVA, crimen ES704 como contexto provincial)
- **Callejero municipal** (base geoespacial, 15 recursos)
- **Sitycleta/Moxsi** (bike sharing stations, ya catalogado)
- **Centros educativos** (ISTAC, geolocalizados)
- **Analítica urbana** (conteo personas mercados, live)
- **Cross-queries**: renta × secciones × barrios × PGO (spatial join verde por barrio)
