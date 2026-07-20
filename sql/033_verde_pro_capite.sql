-- Spazio verde pro-capite LPGC
-- Incrocia PGO (zonizzazione) + popolazione ISTAC
WITH verde AS (
  SELECT sum(ST_Area(geom)) as area_m2
  FROM read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet')
  WHERE TXTPLAN LIKE '%Espacios Libres%'
),
pop AS (
  SELECT value as abitanti
  FROM read_parquet('parquet/poblacion/poblacion_serie_historica.parquet')
  WHERE measure_code = 'POBLACION' AND year = 2025
)
SELECT round(area_m2) as mq_verde_totali,
       abitanti,
       round(area_m2 / abitanti, 1) as mq_verde_pro_capite
FROM verde, pop
