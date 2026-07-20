-- Composicion por grupos de edad
SELECT
  date AS anio,
  poblacion_00a14 AS jovenes,
  poblacion_15a64 AS adultos,
  poblacion_65mas AS mayores,
  poblacion_indice_dependencia AS indice_dependencia,
  poblacion_indice_vejez AS indice_vejez
FROM read_parquet('parquet/poblacion/indicadores_demograficos.parquet')
ORDER BY date
