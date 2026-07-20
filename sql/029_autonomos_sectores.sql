-- Distribución sectorial de autónomos en LPGC (2025)
-- ¿En qué sectores económicos trabajan los autónomos?
-- Fuente: ISTAC E58015B_000054

WITH ultimo_anio AS (
    SELECT max(year) AS anio
    FROM read_parquet('parquet/economia/autonomos_sectores_lpgc.parquet')
),
sectores AS (
    SELECT sector, sector_code,
           round(avg(valor), 0) AS media_autonomos
    FROM read_parquet('parquet/economia/autonomos_sectores_lpgc.parquet')
    WHERE year = (SELECT anio FROM ultimo_anio)
      AND valor IS NOT NULL
    GROUP BY sector, sector_code
),
total AS (
    SELECT round(sum(media_autonomos), 0) AS total_autonomos
    FROM sectores
)
SELECT s.sector,
       s.sector_code,
       s.media_autonomos,
       round(s.media_autonomos * 100.0 / t.total_autonomos, 1) AS pct
FROM sectores s, total t
ORDER BY media_autonomos DESC;
