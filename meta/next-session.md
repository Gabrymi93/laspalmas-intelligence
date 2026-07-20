# Próxima sesión

## Estado actual (2026-07-20)
- **12 scripts ingest, 35 queries, 24 datasets**
- Cross-domain joins: renta×poblacion×distrito, verde×barrio/distrito, paro×renta, incidentes×paro
- **Fix aplicado**: ST_Transform requiere dos SRID + ST_FlipCoordinates en DuckDB v1.5.4
- **run_queries.py** reescrito: soporte multi-resultado, sin pandas
- **35 queries verificadas (0 errores)**

## Nuevas queries incorporadas (10)

| # | Query | Hallazgo principal |
|---|-------|-------------------|
| 009 | `incidentes_horario` | 65.6% accidentes 12-24h, pico viernes, valle agosto |
| 013 | `paro_juvenil_barrio` | Hasta 50% paro juvenil en La Palma y Lomo El Sabinal |
| 014 | `envejecimiento_distrito` | D03 índice 253.7 vs D05 100.3 |
| 015 | `verde_vs_renta` | D01 lidera verde (2.21 km²) con paro más alto (25.1%) |
| 016 | `incidentes_tipo` | 81.5% colisiones, atropellos más graves (1.09 heridos) |
| 017 | `gtfs_sitycleta` | 10/11 estaciones a <100m de parada guagua |
| 018 | `incidentes_vs_paro` | Paro +45% → accidentes -22% (2008-2013) |
| 023 | `estacionalidad_turistica` | Dos picos: enero y agosto, valle mayo (-24%) |
| 024 | `paro_por_edad` | El paro envejece: 60+ lidera desde 2022 |
| 025 | `paro_por_sexo` | Brecha género 134.9 (mujeres 57% del paro) |

## Quick wins pendientes (A)
- **Sensores calidad del aire** — dataset `940cc41a-4e25-4c3d-8d96-ad1047420919`, 3 recursos, live
- **Callejero municipal** — dataset `d33b9b2a-144a-45a9-b3bb-652d384e2a7a`, 15 recursos
- **Centros educativos** — dataset `centros-educativos-de-canarias` (ISTAC, 4 recursos)
- **Analítica urbana** — dataset `1de68939-e54e-4bcc-8a7a-64263e593b00`, conteo mercados

## Gap queries (B)
- **019**: espacio libre (sugerencia: accidentes por calle usando el callejero)
- **026-029**: espacio libre (sugerencia: calidad del aire, contexto Eurostat)

## Bloqueos conocidos
- **Sitycleta Moxsi 2026** — GeoJSON en ckan.laspalmasgc.es (timeout/403), solo datos 2018
- **Atestados 2017+** — no publicados. Último año: 2016
- **GTFS stops OSM** — Overpass API rate-limiting, script listo con retry
- **ST_Transform PROJ** — DuckDB v1.5.4 requiere ST_FlipCoordinates + dos SRID (solucionado)

## A futuro (C)
- **Ingerir sensores calidad del aire** — script ingest pendiente
- **Ingerir callejero municipal** — para geolocalizar incidentes por distrito/barrio
- **Eurostat NUTS-3** (ES704) — PIL, GVA, crimen como contexto provincial
- **Visualización**: mapas barrio/indicador con DuckDB spatial + export GeoJSON
- **CI/CD**: GitHub Actions para refresh semanal
- **Evaluar apertura del repo** (público)

## Notas técnicas
- DuckDB CLI v1.2.1 (obsoleto) ↔ DuckDB Python v1.5.4 (usado por run_queries.py)
- ST_Transform necesita: `ST_Transform(ST_FlipCoordinates(geom), 'EPSG:4326', 'EPSG:32628')`
- `make queries` usa `python3 ingest/run_queries.py` (NO duckdb CLI)
- `make refresh` usa scripts Python individuales
