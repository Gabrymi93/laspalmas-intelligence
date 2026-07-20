-- Evolución de autónomos en LPGC (2010-2026)
-- Target principal del coworking: trabajadores por cuenta propia
-- Fuente: ISTAC E58015B_000054 + C00069A_000005

SELECT year,
       round(avg(valor), 0) AS autonomos_medios,
       min(valor) AS minimo,
       max(valor) AS maximo,
       count(*) AS periodos
FROM read_parquet('parquet/economia/autonomos_lpgc.parquet')
GROUP BY year
ORDER BY year;
