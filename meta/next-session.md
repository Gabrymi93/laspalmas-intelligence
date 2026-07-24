# Próxima sesión

## Estado actual (2026-07-24)
- **12 scripts ingest, 41 queries, 26 datasets**
- **make all**: refresh → validate (21 datasets) → queries (41, 0 errores) → status
- CI/CD: refresh semanal (lun 6:00) + validación PR (ci.yml)
- Repo público: MIT, badge CI+refresh, CONTRIBUTING, disclaimer

## Fix aplicados en esta sesión
- refresh.yml: fail-closed (sin `|| echo`), añadidos targets faltantes
- bin/validate.py: 21 datasets con checks (rows, año, existencia)
- 018 renombrado: "correlación" → "comparación temporal" + disclaimer
- istac_empresas.py: fix paréntesis en máscara Pandas
- meta/catalog.json: eliminado duplicado sitycleta, documentación alineada
- README: 41 queries, estructura actualizada, pendiente realista
- Catalogos locales removidos (API CKAN live bastan)

## Quick wins pendientes (A)
- **Centros educativos** — dataset ISTAC, geolocalizados
- **Sensores calidad del aire** — dataset `940cc41a-4e25-4c3d-8d96-ad1047420919`, 3 recursos, live
- **Analítica urbana** — dataset `1de68939-e54e-4bcc-8a7a-64263e593b00`, conteo mercados
- **Eurostat NUTS-3** (ES704) — PIL, GVA, crimen como contexto provincial

## Bloqueos conocidos
- **Sitycleta Moxsi 2026** — GeoJSON en ckan.laspalmasgc.es (timeout/403), solo datos 2018
- **Atestados 2017+** — no publicados. Último año: 2016
- **Callejero geometría** — ArcGIS REST no expone geometrías públicamente

## A futuro (C)
- Validación más fina: schema checks, outliers, tests unitarios por script
- Visualización: mapas barrio/indicador con DuckDB spatial
- Documentación metodológica para queries (no solo resultados)
- Evaluar esquema de versionado para parquet (no LFS ahora)
