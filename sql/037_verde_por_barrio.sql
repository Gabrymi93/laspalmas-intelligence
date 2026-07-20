-- Spazi verdi per barrio: intersezione spaziale PGO ZUSO (Espacios Libres) con Barrios
WITH verde AS (
    SELECT b.label as barrio,
           sum(ST_Area(ST_Intersection(ST_Transform(b.geometry, 'EPSG:32628'), z.geom))) as verde_m2
    FROM read_parquet('parquet/geografia/barrios_lpgc.parquet') b
    JOIN read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet') z
      ON ST_Intersects(ST_Transform(b.geometry, 'EPSG:32628'), z.geom)
    WHERE z.TXTPLAN LIKE '%Libres%'
    GROUP BY b.label
),
barrios AS (
    SELECT label, pact_t
    FROM read_parquet('parquet/geografia/dim_barrios.parquet')
    WHERE pact_t IS NOT NULL
)
SELECT v.barrio,
       round(v.verde_m2) as verde_m2,
       b.pact_t as poblacion_activa,
       round(v.verde_m2 / NULLIF(b.pact_t, 0), 1) as m2_por_activo
FROM verde v
JOIN barrios b ON v.barrio = b.label
ORDER BY m2_por_activo DESC
LIMIT 15;
