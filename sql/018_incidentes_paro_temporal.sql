-- Comparación temporal: accidentes de tráfico vs desempleo en LPGC (2008-2013)
-- Muestra las dos series lado a lado. No es un análisis de correlación:
-- solo 6 observaciones, posibles confundentes (crisis económica, movilidad, etc.)
-- Fuente: Atestados Policía Local + ISTAC Paro Registrado

WITH incidentes AS (
    SELECT year,
           count(*) AS total_accidentes,
           sum(CASE WHEN HERIDOS > 0 THEN 1 ELSE 0 END) AS con_heridos,
           sum(CASE WHEN HERIDOS = 0 THEN 1 ELSE 0 END) AS sin_heridos,
           round(avg(HERIDOS), 3) AS media_heridos,
           sum(CAST(HERIDOS AS INTEGER)) AS total_heridos
    FROM read_parquet('parquet/movilidad/atestados_acc.parquet')
    WHERE year >= 2008 AND year <= 2013
    GROUP BY year
),
paro_anual AS (
    SELECT CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\d{4})', 1) AS INTEGER) AS anno,
           SUM(OBS_VALUE) AS paro_medio_anual
    FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
    WHERE EDAD_CODE = '_T' AND SEXO_CODE = '_T' AND TERRITORIO_CODE = 35016
    GROUP BY anno
)
SELECT i.year,
       i.total_accidentes,
       i.con_heridos,
       i.sin_heridos,
       i.media_heridos,
       i.total_heridos,
       p.paro_medio_anual,
       round(p.paro_medio_anual * 1.0 / i.total_accidentes, 1) AS paro_por_accidente,
       round((i.total_accidentes - lag(i.total_accidentes) OVER (ORDER BY i.year)) * 100.0 / 
             NULLIF(lag(i.total_accidentes) OVER (ORDER BY i.year), 0), 1) AS var_accidentes_pct,
       round((p.paro_medio_anual - lag(p.paro_medio_anual) OVER (ORDER BY p.anno)) * 100.0 / 
             NULLIF(lag(p.paro_medio_anual) OVER (ORDER BY p.anno), 0), 1) AS var_paro_pct
FROM incidentes i
JOIN paro_anual p ON i.year = p.anno
ORDER BY i.year;
