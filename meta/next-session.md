# Próxima sesión

## Estado actual (2026-07-20)
- 12 scripts ingest, 25 queries, 24 datasets
- Cross-domain joins funcionales: renta×poblacion×distrito, verde×barrio/distrito, paro×renta
- Todos los queries verificados (0 errores)

## Quick wins pendientes (A)
- **Sensores calidad del aire** — dataset `940cc41a-4e25-4c3d-8d96-ad1047420919`, 3 recursos, live
- **Callejero municipal** — dataset `d33b9b2a-144a-45a9-b3bb-652d384e2a7a`, 15 recursos
- **Centros educativos** — dataset `centros-educativos-de-canarias` (ISTAC, 4 recursos)
- **Analítica urbana** — dataset `1de68939-e54e-4bcc-8a7a-64263e593b00`, conteo mercados

## Bloqueos conocidos
- **Sitycleta Moxsi 2026** — GeoJSON en ckan.laspalmasgc.es (timeout/403), solo datos 2018 disponibles
- **Atestados 2017+** — no publicados. Último año: 2016
- **GTFS stops OSM** — Overpass API rate-limiting, script `fetch_gtfs_stops.py` listo con retry

## A futuro (C)
- CI/CD con GitHub Actions para refresh semanal
- Schema estable para consumo desde osint-canarias
- Evaluar apertura del repo (publico)
- Eurostat NUTS-3 contexto (ES704)

## Notas técnicas
- DuckDB v1.5.4, spatial extension para GeoParquet
- `read_parquet(filename=true)` columna se llama `filename`
- WFS Indicadores Demograficos: `https://datos.canarias.es/api/estadisticas/geographical-resources/indicadoresdemograficos/ows`
- CQL filter: `geocode LIKE '%_35016_%'` (single quotes)
