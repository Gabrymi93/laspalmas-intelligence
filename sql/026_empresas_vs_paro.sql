-- Relación entre micro-empresas (1-9 asalariados) y desempleo en LPGC
-- ¿Cuándo sube el paro, bajan las micro-empresas?
-- Fuente: ISTAC Empresas + Paro Registrado

WITH micro AS (
    SELECT year, round(avg(valor), 0) AS micro_empresas
    FROM read_parquet('parquet/economia/empresas_lpgc.parquet')
    WHERE estrato_code = '1T9' AND valor IS NOT NULL AND valor > 0
    GROUP BY year
),
paro AS (
    SELECT CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\d{4})', 1) AS INTEGER) AS anno,
           AVG(OBS_VALUE) AS paro_medio
    FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
    WHERE EDAD_CODE = '_T' AND SEXO_CODE = '_T' AND TERRITORIO_CODE = 35016
    GROUP BY anno
)
SELECT m.year, m.micro_empresas,
       round(p.paro_medio, 0) AS paro_medio_mensual,
       round((m.micro_empresas - lag(m.micro_empresas) OVER (ORDER BY m.year)) * 100.0 /
             NULLIF(lag(m.micro_empresas) OVER (ORDER BY m.year), 0), 1) AS var_micro_pct,
       round((p.paro_medio - lag(p.paro_medio) OVER (ORDER BY p.anno)) * 100.0 /
             NULLIF(lag(p.paro_medio) OVER (ORDER BY p.anno), 0), 1) AS var_paro_pct
FROM micro m
JOIN paro p ON m.year = p.anno
ORDER BY m.year;
