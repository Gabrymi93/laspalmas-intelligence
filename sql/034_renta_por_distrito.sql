-- Renta per distrito 2023: composicion de ingresos por fuente
WITH renta_distrito AS (
    SELECT h.distrito_code, h.distrito_label, r.medida_code,
           round(avg(r.valor), 1) as pct
    FROM read_parquet('parquet/economia/renta_secciones_lpgc.parquet') r
    JOIN read_parquet('parquet/geografia/dim_hierarchy.parquet') h
      ON r.seccion_code = h.seccion_code
    WHERE r.year = 2023
    GROUP BY h.distrito_code, h.distrito_label, r.medida_code
)
SELECT distrito_label,
       max(CASE WHEN medida_code='SUELDOS_SALARIOS' THEN pct END) as sueldos,
       max(CASE WHEN medida_code='PENSIONES' THEN pct END) as pensiones,
       max(CASE WHEN medida_code='OTROS_INGRESOS' THEN pct END) as otros_ingresos,
       max(CASE WHEN medida_code='PRESTACIONES_DESEMPLEO' THEN pct END) as prest_desempleo,
       max(CASE WHEN medida_code='OTRAS_PRESTACIONES' THEN pct END) as otras_prestaciones
FROM renta_distrito
GROUP BY distrito_label
ORDER BY distrito_label;
