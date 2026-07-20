-- Resumen de todos los planes urbanisticos en el repositorio
SELECT
  replace(fname, '_ZUSO.parquet', '') AS plan_id,
  COUNT(*) AS poligonos_zonificacion
FROM (SELECT DISTINCT filename AS fname FROM glob('parquet/urbanismo/*_ZUSO.parquet')) files,
     read_parquet(files.fname)
GROUP BY fname
ORDER BY poligonos_zonificacion DESC
