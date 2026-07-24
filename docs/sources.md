# Fuentes de datos

| Fuente | Tipo | Datasets | Acceso |
|--------|------|----------|--------|
| **ISTAC** (datos.canarias.es) | CKAN + REST API | ~22K datasets | CSV/TSV/JSON vía API REST |
| **Ayuntamiento LPGC** (datosabiertos.laspalmasgc.es) | WordPress/Viavansi | ~200 datasets | DCAT RDF + CKAN DataStore API |
| **SITCAN** (opendata.sitcan.es) | CKAN geo | 174 datasets | Descarga ZIP (SHP) |
| **Eurostat** | SDMX | 28 datasets NUTS-3 | MCP connector |

## Endpoints API

### ISTAC
- **CKAN**: `https://datos.canarias.es/catalogos/estadisticas/api/3/action`
- **REST (cubos estadísticos)**: `https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/{CUBO}/{VERSION}.csv`
- **WFS (geografía)**: `https://datos.canarias.es/api/estadisticas/geographical-resources/indicadoresdemograficos/ows`

### Ayuntamiento LPGC
- **CKAN DataStore**: `http://apidatosabiertos.laspalmasgc.es/api/3/action`
- **DCAT RDF**: `http://datosabiertos.laspalmasgc.es/proxyFileCKAN.php?catalog=http://datosabiertos.laspalmasgc.es/catalog.rdf`
- **ArcGIS REST**: `https://sit.laspalmasgc.es/server/rest/services/opendata/{capa}/MapServer`

### SITCAN
- **CKAN**: `https://opendata.sitcan.es/api/3/action`

## Scripts de ingest

Cada script en `ingest/` descarga de una fuente y produce archivos Parquet en `parquet/`.

| Script | Fuente | Dataset |
|--------|--------|---------|
| `istac_population.py` | ISTAC | Población histórica |
| `istac_employment.py` | ISTAC | Paro registrado |
| `istac_renta.py` | ISTAC | Renta bruta |
| `istac_empresas.py` | ISTAC | Empresas por tamaño |
| `istac_autonomos.py` | ISTAC | Autónomos (cuenta propia) |
| `fetch_tourism.py` | ISTAC | Turismo (ocupación, pernoctaciones, gasto) |
| `fetch_poblacion_secciones.py` | ISTAC WFS | Población por sección censal |
| `fetch_geografia_wfs.py` | ISTAC WFS | Distritos, barrios, secciones |
| `fetch_urbanismo_sitcan.py` | SITCAN | PGO, planeamiento |
| `fetch_gtfs.py` | Ayto LPGC | GTFS (rutas, viajes, horarios) |
| `fetch_atestados.py` | Ayto LPGC | Atestados policía (accidentes) |
| `fetch_sitycleta.py` | Ayto LPGC | Estaciones Sitycleta |
| `fetch_callejero.py` | Ayto LPGC | Callejero municipal |
| `fetch_gtfs_stops.py` | OSM / Overpass | Coordenadas de paradas GTFS |
