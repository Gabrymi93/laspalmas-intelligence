-- Poblacion por sexo (indicadores demograficos 2008-2022)
SELECT
  date AS anio,
  poblacion_hombres AS hombres,
  poblacion_mujeres AS mujeres,
  poblacion AS total
FROM read_parquet('parquet/poblacion/indicadores_demograficos.parquet')
ORDER BY date
