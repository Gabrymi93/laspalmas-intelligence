-- Resumen de todos los planes urbanisticos en el repositorio
SELECT regexp_extract(filename, '([^/]+)_ZUSO', 1) AS plan_id,
       count(*) AS poligonos_zonificacion
FROM read_parquet('parquet/urbanismo/*_ZUSO.parquet', filename=true)
GROUP BY filename
ORDER BY poligonos_zonificacion DESC;
