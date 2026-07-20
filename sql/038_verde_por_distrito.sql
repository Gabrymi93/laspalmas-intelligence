-- Spazi verdi per distretto: intersezione PGO Espacios Libres con Distritos
SELECT d.label as distrito,
       round(sum(ST_Area(ST_Intersection(ST_Transform(ST_FlipCoordinates(d.geometry), 'EPSG:4326', 'EPSG:32628'), z.geom)))) as verde_m2,
       d.pact_t as activos,
       round(sum(ST_Area(ST_Intersection(ST_Transform(ST_FlipCoordinates(d.geometry), 'EPSG:4326', 'EPSG:32628'), z.geom))) / d.pact_t, 1) as m2_por_activo
FROM read_parquet('parquet/geografia/distritos_lpgc.parquet') d
JOIN read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet') z
  ON ST_Intersects(ST_Transform(ST_FlipCoordinates(d.geometry), 'EPSG:4326', 'EPSG:32628'), z.geom)
WHERE z.TXTPLAN LIKE '%Libres%'
GROUP BY d.label, d.pact_t
ORDER BY m2_por_activo DESC;
