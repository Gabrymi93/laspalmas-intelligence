# Próxima sesión — Plan de trabajo

## Novedades de esta sesión

- ✅ Escaneo sistemático de los 180 datasets del portal Ayuntamiento LPGC
- ✅ Escaneo ISTAC: descubiertos datasets de renta por sección censal (granularidad sub-municipal)
- ✅ Ingerido renta bruta por municipio LPGC (45 rows, 2015-2023, 5 fuentes de ingreso)
- ✅ Ingerido renta bruta por sección censal (12.395 rows, 281 secciones, 2015-2023)
- ✅ Ingerido atestados policía local (76.178 accidentes, 45.488 heridos, 148.650 vehículos, 1998-2016)

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
- Ahora tenemos renta por sección censal → podemos cruzar con población por sección (INE)

### P1 — Sensores calidad del aire
- Dataset Viavansi, actualizado 2026-07-17
- Verificar si tiene datastore_active en apidatosabiertos
- Dataset `940cc41a-4e25-4c3d-8d96-ad1047420919` tiene 3 recursos

### P1 — Sitycleta/Moxsi (bike sharing)
- Dataset `15ef40e1-6974-4688-a0bf-40bbd4160018`
- 1 recurso con datastore_active
- Ya catalogado, falta ingerir

### P1 — Callejero municipal
- Dataset `d33b9b2a-144a-45a9-b3bb-652d384e2a7a`
- 15 recursos, base geoespacial vías/números
- Ya catalogado, falta ingerir

### P2 — Stops GTFS (coordenadas paradas)
- 844 stop_ids conocidos, faltan lat/lon
- Alternativas: OSM Overpass API, cache Google Transit

### P2 — Eurostat NUTS-3 contexto
- Población, PIL, GVA, crimen para ES704
- Disponible vía MCP eurostat

### P3 — Centros educativos
- ISTAC dataset `centros-educativos-de-canarias`
- 4 recursos, geolocalizado

### P3 — Analítica urbana (conteo personas mercados)
- Dataset `1de68939-e54e-4bcc-8a7a-64263e593b00`
- Live data, 2 recursos

## Notas técnicas

- API DataStore: `http://apidatosabiertos.laspalmasgc.es/api/3/action/`
- WFS ISTAC: `https://datos.canarias.es/api/estadisticas/geographical-resources/epareg/ows`
- Capas WFS disponibles: Barrios-{2011..2024}, Distritos-{2011..2024}, Comarcas-{2011..2024}
- Ejemplo WFS: `?service=WFS&version=1.1.0&request=GetFeature&typeName=Barrios-2024&outputFormat=application/json`
- DuckDB spatial: `ST_Intersects` para cruzar geometrías entre capas
- Renta secciones: TERRITORIO_CODE formato `YYYYMMDD_35016_DXX_SXXX`
- Atestados: tres tablas (acc, her, veh) vinculadas por campo DILIG dentro de cada año
