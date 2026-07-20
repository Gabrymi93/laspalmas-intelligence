-- Estacionalidad turística: pernoctaciones mensuales en Gran Canaria (2010-2026)
-- Patrón estacional: meses de mayor y menor demanda turística
-- Fuente: ISTAC Encuesta de Alojamiento Turístico

WITH mensual AS (
    SELECT anno, mese,
           OBS_VALUE AS pernoctaciones,
           CASE mese
               WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero' WHEN 3 THEN 'Marzo'
               WHEN 4 THEN 'Abril' WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
               WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto' WHEN 9 THEN 'Septiembre'
               WHEN 10 THEN 'Octubre' WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
           END AS mes_label
    FROM read_parquet('parquet/turismo/pernottamenti_gran_canaria.parquet')
    WHERE anno >= 2010
),
-- Perfil estacional promedio (todos los años)
perfil_estacional AS (
    SELECT mese, mes_label,
           round(avg(pernoctaciones), 0) AS media_pernoctaciones,
           round(stddev(pernoctaciones), 0) AS desviacion,
           round(min(pernoctaciones), 0) AS minimo,
           round(max(pernoctaciones), 0) AS maximo,
           -- Índice estacional: 100 = media anual
           round(avg(pernoctaciones) * 100.0 / 
                 (SELECT avg(pernoctaciones) FROM mensual), 1) AS indice_estacional
    FROM mensual
    GROUP BY mese, mes_label
)
SELECT
    mes_label AS mes,
    media_pernoctaciones,
    desviacion,
    minimo,
    maximo,
    indice_estacional,
    CASE
        WHEN indice_estacional > 110 THEN 'Alta'
        WHEN indice_estacional BETWEEN 90 AND 110 THEN 'Media'
        ELSE 'Baja'
    END AS temporada
FROM perfil_estacional
ORDER BY mese;
