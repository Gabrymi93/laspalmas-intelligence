-- Paro por grupo de edad (ultimo mes disponible)
SELECT
  EDAD_CODE AS grupo_edad,
  OBS_VALUE AS paro
FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
WHERE SEXO_CODE = '_T'
  AND EDAD_CODE != '_T'
  AND TIME_PERIOD_CODE = (SELECT MAX(TIME_PERIOD_CODE) FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet'))
ORDER BY EDAD_CODE
