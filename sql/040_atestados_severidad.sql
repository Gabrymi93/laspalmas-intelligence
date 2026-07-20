-- Evolucion de la severidad de accidentes (2000-2016): proporcion de heridos graves
WITH anual AS (
    SELECT a.year,
           count(DISTINCT a.dilig) as accidentes,
           count(h.dilig) as heridos,
           sum(CASE WHEN h.lesividad = 'Grave' THEN 1 ELSE 0 END) as graves,
           sum(CASE WHEN h.lesividad = 'Leve' THEN 1 ELSE 0 END) as leves,
           sum(CASE WHEN h.lesividad = 'Fallecido' THEN 1 ELSE 0 END) as fallecidos
    FROM read_parquet('parquet/movilidad/atestados_acc.parquet') a
    JOIN read_parquet('parquet/movilidad/atestados_her.parquet') h ON a.dilig = h.dilig AND a.year = h.year
    WHERE a.year >= 2000
    GROUP BY a.year
)
SELECT year, accidentes, heridos, graves, leves, fallecidos,
       round(100.0 * graves / heridos, 1) as graves_pct,
       round(100.0 * fallecidos / heridos, 2) as fallecidos_pct
FROM anual
ORDER BY year;
