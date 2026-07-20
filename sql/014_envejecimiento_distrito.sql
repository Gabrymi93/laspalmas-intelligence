-- Estructura de edad por distrito (2022)
-- Agrega datos de secciones censales a nivel de distrito
-- Indicadores: índice de envejecimiento, dependencia, % mayores
-- Fuente: ISTAC Indicadores demográficos por secciones + dimensiones

WITH secciones AS (
    SELECT
        s.seccion_code,
        s.poblacion,
        s.poblacion_00a14,
        s.poblacion_15a64,
        s.poblacion_65mas,
        s.poblacion_edad_media,
        s.poblacion_indice_dependencia,
        s.poblacion_extranjera
    FROM read_parquet('parquet/poblacion/poblacion_secciones.parquet') s
    WHERE s.year = 2022
),
distritos AS (
    SELECT
        h.distrito_code,
        h.distrito_label,
        sum(s.poblacion) AS poblacion_total,
        sum(s.poblacion_00a14) AS jovenes,
        sum(s.poblacion_15a64) AS adultos,
        sum(s.poblacion_65mas) AS mayores,
        sum(s.poblacion_extranjera) AS extranjeros,
        round(avg(s.poblacion_edad_media), 1) AS edad_media,
        -- Índice de envejecimiento: mayores / jóvenes * 100
        CASE
            WHEN sum(s.poblacion_00a14) > 0
            THEN round(sum(s.poblacion_65mas) * 100.0 / sum(s.poblacion_00a14), 1)
            ELSE NULL
        END AS indice_envejecimiento,
        -- Índice de dependencia: (jóvenes+mayores) / adultos * 100
        CASE
            WHEN sum(s.poblacion_15a64) > 0
            THEN round((sum(s.poblacion_00a14) + sum(s.poblacion_65mas)) * 100.0 / sum(s.poblacion_15a64), 1)
            ELSE NULL
        END AS indice_dependencia,
        -- % población mayor de 65
        CASE
            WHEN sum(s.poblacion) > 0
            THEN round(sum(s.poblacion_65mas) * 100.0 / sum(s.poblacion), 1)
            ELSE NULL
        END AS pct_mayores,
        -- % población extranjera
        CASE
            WHEN sum(s.poblacion) > 0
            THEN round(sum(s.poblacion_extranjera) * 100.0 / sum(s.poblacion), 1)
            ELSE NULL
        END AS pct_extranjeros
    FROM secciones s
    JOIN read_parquet('parquet/geografia/dim_hierarchy.parquet') h
        ON s.seccion_code = h.seccion_code
    GROUP BY h.distrito_code, h.distrito_label
)
SELECT
    distrito_label AS distrito,
    poblacion_total,
    jovenes,
    adultos,
    mayores,
    edad_media,
    indice_envejecimiento,
    indice_dependencia,
    pct_mayores,
    pct_extranjeros
FROM distritos
ORDER BY indice_envejecimiento DESC;
