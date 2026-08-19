# Próxima sesión

## Estado actual (2026-08-13)
- **15 scripts ingest, 44 queries, 29 datasets**
- **make all**: refresh → validate (24 datasets) → queries (44, 0 errores) → status
- CI/CD: refresh semanal (lun 6:00) + validación PR (ci.yml)
- Repo público: MIT, badge CI+refresh, CONTRIBUTING, disclaimer
- **Nuevo**: sensores de calidad del aire (Gemelo Digital) — 3 datasets en `parquet/ambiente/`

## Hecho en la sesión 2026-08-13
- ingest/fetch_calidad_aire.py: 2 recursos CKAN DataStore + ArcGIS FeatureServer
  - sensores propios (R1): 7.725 lecturas, 4 sensores, Mercado Central + Puerto, 2026-05→07
  - estaciones Gob. de Canarias (R2): 118.840 lecturas, 4 estaciones × 7 parámetros, 2025-07→2026-05
  - ubicación estaciones (geo): 4 estaciones lat/lon desde FeatureServer EstacionesCalidadAire
- **Fix importante**: datastore_search con paginación offset devuelve duplicados (31k en R2).
  Se usa datastore_search_sql + ORDER BY _id (determinista, verificado 118.840/118.840 distintos)
- Makefile target `aire`, validate + status + queries #042-044, docs y catalog.json actualizados

## Quick wins pendientes (A)
- **Centros educativos** — dataset ISTAC, geolocalizados
- **Analítica urbana** — dataset `1de68939-e54e-4bcc-8a7a-64263e593b00`, conteo mercados
- **Eurostat NUTS-3** (ES704) — PIL, GVA, crimen como contexto provincial

## Bloqueos conocidos
- **Sitycleta Moxsi 2026** — GeoJSON en ckan.laspalmasgc.es (timeout/403), solo datos 2018
- **Atestados 2017+** — no publicados. Último año: 2016
- **Callejero geometría** — ArcGIS REST no expone geometrías públicamente
- **Calidad aire GeoJSON** (ckan.laspalmasgc.es) — timeout; se usa FeatureServer en su lugar

## A futuro (C)
- Validación más fina: schema checks, outliers, tests unitarios por script
- Visualización: mapas barrio/indicador con DuckDB spatial
- Documentación metodológica para queries (no solo resultados)
- Evaluar esquema de versionado para parquet (no LFS ahora)
