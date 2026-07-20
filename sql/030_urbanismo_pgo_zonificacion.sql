-- Zonificacion del PGO (Plan General de Ordenacion) de LPGC
-- 6.608 poligonos de clasificacion del suelo
SELECT
  CODIGO,
  ETIQUETA AS etiqueta_urbanistica,
  TXTPLAN AS texto_plan
FROM read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet')
ORDER BY CODIGO
