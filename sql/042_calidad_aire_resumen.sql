-- Resumen de los sensores de calidad del aire (proyecto Gemelo Digital LPGC)
-- Fuentes: CKAN DataStore ayuntamiento LPGC (sensores-de-calidad-del-aire) + ArcGIS FeatureServer
-- Valores de sensores propios: lecturas crudas (sin corrección de escala)

SELECT 'ESTACIONES GOBIERNO CANARIAS' AS seccion, CAST(count(*) AS VARCHAR) AS valor
FROM read_parquet('parquet/ambiente/calidad_aire_estaciones_geo.parquet')
UNION ALL
SELECT 'LECTURAS ESTACIONES', CAST(count(*) AS VARCHAR)
FROM read_parquet('parquet/ambiente/calidad_aire_estaciones.parquet')
UNION ALL
SELECT 'SENSORES PROPIOS (MERCADOS)', CAST(count(*) AS VARCHAR)
FROM read_parquet('parquet/ambiente/calidad_aire_gemelo.parquet')
UNION ALL
SELECT 'MERCADOS CON SENSORES', string_agg(DISTINCT mercado, ', ')
FROM read_parquet('parquet/ambiente/calidad_aire_gemelo.parquet')
UNION ALL
SELECT 'PARAMETROS MEDIDOS', string_agg(DISTINCT nombre_parametro, ' | ')
FROM read_parquet('parquet/ambiente/calidad_aire_estaciones.parquet')
UNION ALL
SELECT 'PERIODO ESTACIONES', min(datetime)::VARCHAR || ' -> ' || max(datetime)::VARCHAR
FROM read_parquet('parquet/ambiente/calidad_aire_estaciones.parquet')
ORDER BY 1;
