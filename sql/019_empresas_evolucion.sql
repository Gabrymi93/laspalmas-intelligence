-- Evolución del tejido empresarial de LPGC por tamaño (2005-2015)
-- Muestra cómo cambia la composición: micro-empresas vs pequeñas vs grandes
-- Fuente: ISTAC Empresas por estrato de asalariados

WITH anual AS (
    SELECT year,
           estrato_code, estrato_label,
           round(avg(valor), 0) AS media_anual
    FROM read_parquet('parquet/economia/empresas_lpgc.parquet')
    WHERE estrato_code != '_T' AND valor IS NOT NULL AND valor > 0
    GROUP BY year, estrato_code, estrato_label
),
total_anual AS (
    SELECT year, round(avg(valor), 0) AS total_empresas
    FROM read_parquet('parquet/economia/empresas_lpgc.parquet')
    WHERE estrato_code = '_T' AND valor IS NOT NULL AND valor > 0
    GROUP BY year
)
SELECT a.year,
       a.estrato_label,
       a.media_anual,
       round(a.media_anual * 100.0 / t.total_empresas, 1) AS pct_sobre_total,
       t.total_empresas
FROM anual a
JOIN total_anual t ON a.year = t.year
ORDER BY a.year, a.estrato_code;
