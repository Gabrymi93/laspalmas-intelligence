-- Paro registrado por sexo (serie mensual)
SELECT
  a.TIME_PERIOD_CODE AS mes,
  a.OBS_VALUE AS hombres,
  b.OBS_VALUE AS mujeres
FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet') a
JOIN read_parquet('parquet/empleo/paro_sexo_edad.parquet') b
  ON a.TIME_PERIOD_CODE = b.TIME_PERIOD_CODE
WHERE a.SEXO_CODE = 'M' AND a.EDAD_CODE = '_T'
  AND b.SEXO_CODE = 'F' AND b.EDAD_CODE = '_T'
ORDER BY a.TIME_PERIOD_CODE
