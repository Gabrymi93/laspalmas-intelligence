# Próxima sesión — Plan de trabajo

## Novedades de esta sesión

- ✅ SITCAN urbanismo: 39/40 SIPU descargados y convertidos a GeoParquet
- ✅ PGO (Plan General de Ordenación): 6.608 poligonos ZUSO, 821 CAT
- ✅ Primera query cross-fonte: verde pro-capite LPGC (13,4 m²/hab)
- ✅ Descubierto WFS ISTAC con capas Barrios-2011..2024 y Distritos-2011..2024

## Gap crítico identificado

**Población por barrio/distrito**: no tenemos población total desagregada.
- ISTAC tiene "Población. Distritos. 2004-2021" pero solo como mapas temáticos (imágenes WMS)
- Los WFS Barrios/Distritos tienen solo `pact_t` (población activa = 15-64 años), no población total
- Alternativas a explorar: cubos estadísticos ISTAC (buscar "poblacion por barrios" como cubo), INE (padrón por sección censal), o proxy con pact_t

## Prioridades pendientes

### P1 — Población por barrio
- Explorar ISTAC: ¿existe un cubo estadístico de población por barrio/distrito?
- Alternativa: WFS Barrios-2024 tiene geometría + pact_t (población activa, proxy útil)
- Si encontramos dato: intersecar con PGO → verde por barrio

### P1 — Sensores calidad del aire
- Dataset Viavansi, actualizado 2026-07-17
- Verificar si tiene datastore_active en apidatosabiertos

### P2 — Stops GTFS (coordenadas paradas)
- 844 stop_ids conocidos, faltan lat/lon
- Alternativas: OSM Overpass API, cache Google Transit

### P2 — Eurostat NUTS-3 contexto
- Población, PIL, GVA, crimen para ES704
- Disponible vía MCP eurostat

## Notas técnicas

- API DataStore: `http://apidatosabiertos.laspalmasgc.es/api/3/action/`
- WFS ISTAC: `https://datos.canarias.es/api/estadisticas/geographical-resources/epareg/ows`
- Capas WFS disponibles: Barrios-{2011..2024}, Distritos-{2011..2024}, Comarcas-{2011..2024}
- Ejemplo WFS: `?service=WFS&version=1.1.0&request=GetFeature&typeName=Barrios-2024&outputFormat=application/json`
- DuckDB spatial: `ST_Intersects` para cruzar geometrías entre capas
