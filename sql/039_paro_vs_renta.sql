-- Confronto distrettuale: tasso di disoccupazione vs composizione reddito
WITH renta_distrito AS (
    SELECT h.distrito_code,
           round(avg(CASE WHEN r.medida_code = 'SUELDOS_SALARIOS' THEN r.valor END), 1) as sueldos_pct,
           round(avg(CASE WHEN r.medida_code = 'PENSIONES' THEN r.valor END), 1) as pensiones_pct,
           round(avg(CASE WHEN r.medida_code = 'PRESTACIONES_DESEMPLEO' THEN r.valor END), 1) as paro_pct_renta
    FROM read_parquet('parquet/economia/renta_secciones_lpgc.parquet') r
    JOIN read_parquet('parquet/geografia/dim_hierarchy.parquet') h ON r.seccion_code = h.seccion_code
    WHERE r.year = 2022
    GROUP BY h.distrito_code
)
SELECT d.label as distrito, d.tpar_t as tasa_paro, d.pact_t as activos,
       r.sueldos_pct, r.pensiones_pct, r.paro_pct_renta
FROM read_parquet('parquet/geografia/dim_distritos.parquet') d
JOIN renta_distrito r ON d.distrito_code = r.distrito_code
ORDER BY tasa_paro DESC;
