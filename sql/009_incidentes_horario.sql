-- Incidentes viales: patrones temporales (hora, día de semana, mes, evolución anual)
-- Todos los análisis en una sola salida con secciones
-- Fuente: Atestados Policía Local (1998-2016)

WITH base AS (
    SELECT
        DILIG, year,
        CAST(REGEXP_EXTRACT(HORA, '(\d{2})', 1) AS INTEGER) AS hora,
        CAST(REGEXP_EXTRACT(FECHA, '(\d{2})/(\d{2})/(\d{4})', 2) AS INTEGER) AS mes,
        dayofweek(CAST(REGEXP_EXTRACT(FECHA, '(\d{4})', 1) || '-' ||
                       REGEXP_EXTRACT(FECHA, '(\d{2})/(\d{2})/(\d{4})', 2) || '-' ||
                       REGEXP_EXTRACT(FECHA, '(\d{1,2})/(\d{1,2})/(\d{4})', 1) AS DATE)) AS dia_semana,
        HERIDOS, COLISION
    FROM read_parquet('parquet/movilidad/atestados_acc.parquet')
    WHERE year >= 2000 AND FECHA IS NOT NULL
)

SELECT 'ACCIDENTES POR FRANJA HORARIA' AS seccion,
       CASE
           WHEN hora BETWEEN 0 AND 5 THEN '00-06 (madrugada)'
           WHEN hora BETWEEN 6 AND 11 THEN '06-12 (mañana)'
           WHEN hora BETWEEN 12 AND 17 THEN '12-18 (tarde)'
           WHEN hora BETWEEN 18 AND 23 THEN '18-24 (noche)'
       END AS categoria,
       CAST(count(*) AS VARCHAR) AS valor
FROM base WHERE hora IS NOT NULL
GROUP BY seccion, categoria

UNION ALL

SELECT 'ACCIDENTES POR DÍA DE SEMANA' AS seccion,
       CASE dia_semana
           WHEN 0 THEN 'Domingo' WHEN 1 THEN 'Lunes' WHEN 2 THEN 'Martes'
           WHEN 3 THEN 'Miércoles' WHEN 4 THEN 'Jueves' WHEN 5 THEN 'Viernes'
           WHEN 6 THEN 'Sábado'
       END AS categoria,
       round(count(*) * 100.0 / (SELECT count(*) FROM base WHERE dia_semana IS NOT NULL), 1) || '%' AS valor
FROM base WHERE dia_semana IS NOT NULL
GROUP BY seccion, dia_semana

UNION ALL

SELECT 'ACCIDENTES POR MES' AS seccion,
       CASE mes
           WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero' WHEN 3 THEN 'Marzo'
           WHEN 4 THEN 'Abril' WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
           WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto' WHEN 9 THEN 'Septiembre'
           WHEN 10 THEN 'Octubre' WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
       END AS categoria,
       round(count(*) * 100.0 / (SELECT count(*) FROM base WHERE mes IS NOT NULL), 1) || '%' AS valor
FROM base WHERE mes IS NOT NULL
GROUP BY seccion, mes

UNION ALL

SELECT 'EVOLUCIÓN ANUAL 2000-2016' AS seccion,
       CAST(year AS VARCHAR) AS categoria,
       CAST(count(*) AS VARCHAR) || ' acc, media ' || CAST(round(avg(HERIDOS), 2) AS VARCHAR) || ' heridos' AS valor
FROM base WHERE year IS NOT NULL
GROUP BY seccion, year
ORDER BY seccion, categoria;
