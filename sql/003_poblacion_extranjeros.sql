-- Poblacion extranjera LPGC 2008-2022
SELECT
  date AS anio,
  poblacion AS total,
  poblacion_extranjera AS extranjeros,
  poblacion_extranjera_pc AS extranjeros_pct
FROM read_parquet('parquet/poblacion/indicadores_demograficos.parquet')
ORDER BY date
