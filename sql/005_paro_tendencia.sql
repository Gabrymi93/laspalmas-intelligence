-- Tendencia mensual del paro registrado LPGC 2008-2026
SELECT
  TIME_PERIOD_CODE AS mes,
  OBS_VALUE AS paro_total
FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
WHERE SEXO_CODE = '_T' AND EDAD_CODE = '_T'
ORDER BY TIME_PERIOD_CODE
