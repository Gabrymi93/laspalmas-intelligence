-- Paro medio anual LPGC
SELECT
  substr(TIME_PERIOD_CODE, 1, 4) AS anio,
  round(avg(OBS_VALUE), 0) AS paro_medio
FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
WHERE SEXO_CODE = '_T' AND EDAD_CODE = '_T'
GROUP BY anio
ORDER BY anio
