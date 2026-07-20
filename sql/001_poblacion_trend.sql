-- Tendencia poblacion LPGC 1986-2025
SELECT
  year,
  value AS poblacion
FROM read_parquet('parquet/poblacion/poblacion_serie_historica.parquet')
WHERE measure_code = 'POBLACION'
  AND value IS NOT NULL
ORDER BY year
