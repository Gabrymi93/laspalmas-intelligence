-- Incidentes viales: clasificación por tipo de colisión y evolución (2000-2016)
-- Identifica los tipos de accidente más frecuentes y su evolución temporal
-- Fuente: Atestados Policía Local

WITH tipos AS (
    SELECT year, DILIG, HERIDOS, DESTINO,
        CASE
            WHEN COLISION IS NULL THEN 'Sin especificar'
            WHEN COLISION LIKE '%Atropello%' THEN 'Atropello'
            WHEN COLISION LIKE '%Colisi%' THEN 'Colisión'
            WHEN COLISION LIKE '%Salida%' THEN 'Salida de vía'
            WHEN COLISION LIKE '%Vuelco%' THEN 'Vuelco'
            ELSE 'Otros'
        END AS tipo_colision
    FROM read_parquet('parquet/movilidad/atestados_acc.parquet')
    WHERE year >= 2000
)

SELECT 'DISTRIBUCIÓN POR TIPO (2000-2016)' AS seccion,
       tipo_colision AS categoria,
       CAST(count(*) AS VARCHAR) || ' (' || round(count(*) * 100.0 / (SELECT count(*) FROM tipos), 1) || '%, media ' || round(avg(HERIDOS), 2) || ' heridos)' AS valor
FROM tipos
GROUP BY seccion, tipo_colision

UNION ALL

SELECT 'EVOLUCIÓN ANUAL POR TIPO' AS seccion,
       CAST(year AS VARCHAR) AS categoria,
       'Atropellos: ' || CAST(count(*) FILTER (WHERE tipo_colision = 'Atropello') AS VARCHAR) ||
       ', Colisiones: ' || CAST(count(*) FILTER (WHERE tipo_colision = 'Colisión') AS VARCHAR) ||
       ', Salidas: ' || CAST(count(*) FILTER (WHERE tipo_colision = 'Salida de vía') AS VARCHAR) ||
       ', Otros: ' || CAST(count(*) FILTER (WHERE tipo_colision NOT IN ('Atropello', 'Colisión', 'Salida de vía')) AS VARCHAR) AS valor
FROM tipos
GROUP BY seccion, year
ORDER BY seccion, categoria;
