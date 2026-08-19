-- Calidad del aire: resumen por estación y parámetro (Gobierno de Canarias)
-- valor_numerico: lecturas crudas (pueden incluir negativos sin corrección)
-- Las filas con valor_texto 'No disponible' se excluyen de la media

SELECT nombre_estacion AS estacion,
       nombre_parametro AS parametro,
       count(*) AS lecturas,
       round(avg(CAST(valor_numerico AS DOUBLE))
             FILTER (WHERE valor_texto <> 'No disponible'), 2) AS media,
       max(datetime) AS ultima_lectura
FROM read_parquet('parquet/ambiente/calidad_aire_estaciones.parquet')
GROUP BY 1, 2
ORDER BY 1, 2;
