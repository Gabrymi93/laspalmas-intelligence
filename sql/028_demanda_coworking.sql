-- Demanda potencial de coworking en LPGC (2012-2026)
-- Cruza autónomos (cuenta propia) + micro-empresas (1-9 asalariados)
-- + población total para ratio por mil habitantes
-- Fuente: ISTAC E58015B_000054 + E58028A_000005 + población

WITH autonomos AS (
    SELECT year, round(avg(valor), 0) AS autonomos_medios
    FROM read_parquet('parquet/economia/autonomos_lpgc.parquet')
    GROUP BY year
),
micro AS (
    SELECT year, round(avg(valor), 0) AS micro_empresas
    FROM read_parquet('parquet/economia/empresas_lpgc.parquet')
    WHERE estrato_code = '1T9' AND valor IS NOT NULL AND valor > 0
    GROUP BY year
),
poblacion AS (
    SELECT year, value AS poblacion
    FROM read_parquet('parquet/poblacion/poblacion_serie_historica.parquet')
    WHERE measure_code = 'POBLACION'
)
SELECT a.year,
       a.autonomos_medios,
       m.micro_empresas,
       a.autonomos_medios + m.micro_empresas AS demanda_coworking,
       p.poblacion,
       round((a.autonomos_medios + m.micro_empresas) * 1000.0 / p.poblacion, 1) AS demanda_por_mil_hab
FROM autonomos a
JOIN micro m ON a.year = m.year
JOIN poblacion p ON a.year = p.year
ORDER BY a.year;
