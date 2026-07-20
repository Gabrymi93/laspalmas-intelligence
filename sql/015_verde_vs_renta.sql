-- Correlación entre espacio verde y composición de renta por distrito (2022-2023)
-- Cruza datos de zonas verdes (PGO) con renta agregada por distrito
-- Hipótesis: distritos con más renta salarial tienen más metros verdes per cápita
-- Fuente: ISTAC renta por secciones + PGO ZUSO + indicadores laborales

WITH verde_distrito AS (
    SELECT d.label AS distrito_label,
           round(sum(ST_Area(ST_Intersection(
               ST_Transform(ST_FlipCoordinates(d.geometry), 'EPSG:4326', 'EPSG:32628'),
               z.geom
           )))) AS verde_m2,
           d.pact_t AS activos
    FROM read_parquet('parquet/geografia/distritos_lpgc.parquet') d
    JOIN read_parquet('parquet/urbanismo/32ffdaab_ZUSO.parquet') z
        ON ST_Intersects(
            ST_Transform(ST_FlipCoordinates(d.geometry), 'EPSG:4326', 'EPSG:32628'),
            z.geom
        )
    WHERE z.TXTPLAN LIKE '%Libres%'
    GROUP BY d.label, d.pact_t
),
renta_distrito AS (
    SELECT h.distrito_label,
           round(avg(CASE WHEN r.medida_code = 'SUELDOS_SALARIOS' THEN r.valor END), 1) AS sueldos_pct,
           round(avg(CASE WHEN r.medida_code = 'PENSIONES' THEN r.valor END), 1) AS pensiones_pct,
           round(avg(CASE WHEN r.medida_code = 'PRESTACIONES_DESEMPLEO' THEN r.valor END), 1) AS prest_desempleo_pct,
           round(avg(CASE WHEN r.medida_code = 'OTROS_INGRESOS' THEN r.valor END), 1) AS otros_ingresos_pct
    FROM read_parquet('parquet/economia/renta_secciones_lpgc.parquet') r
    JOIN read_parquet('parquet/geografia/dim_hierarchy.parquet') h ON r.seccion_code = h.seccion_code
    WHERE r.year = 2022
    GROUP BY h.distrito_label
),
paro_distrito AS (
    SELECT label AS distrito_label, round(tpar_t, 1) AS tasa_paro, round(tsal_t, 1) AS tasa_salarizacion
    FROM read_parquet('parquet/geografia/dim_distritos.parquet')
)
SELECT v.distrito_label,
       round(v.verde_m2) AS verde_total_m2,
       round(v.verde_m2 / NULLIF(v.activos, 0), 1) AS m2_verde_por_activo,
       r.sueldos_pct,
       r.pensiones_pct,
       r.prest_desempleo_pct,
       r.otros_ingresos_pct,
       p.tasa_paro,
       p.tasa_salarizacion
FROM verde_distrito v
JOIN renta_distrito r ON v.distrito_label = r.distrito_label
JOIN paro_distrito p ON v.distrito_label = p.distrito_label
ORDER BY m2_verde_por_activo DESC;
