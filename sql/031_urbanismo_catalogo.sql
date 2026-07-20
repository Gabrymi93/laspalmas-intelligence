-- Elementos catalogados del PGO (821 elementos protegidos)
SELECT
  CODIGO,
  ETIQUETA,
  TXTPLAN AS descripcion
FROM read_parquet('parquet/urbanismo/32ffdaab_CAT.parquet')
ORDER BY CODIGO
