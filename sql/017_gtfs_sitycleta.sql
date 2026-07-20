-- Complementariedad entre red de guaguas y estaciones de Sitycleta (bike sharing)
-- Calcula la distancia mínima de cada estación Sitycleta a la parada de guagua más cercana
-- Cuántas estaciones están fuera de un radio de 300m de cualquier parada?
-- Fuente: GTFS Guaguas Municipales + Sitycleta

WITH stops AS (
    SELECT stop_id, stop_name, stop_lat, stop_lon
    FROM read_parquet('parquet/movilidad/gtfs_stops.parquet')
    WHERE stop_lat IS NOT NULL AND stop_lon IS NOT NULL
),
sitycleta AS (
    SELECT _id as station_id, Nombre, Calle, Latitud, Longitud
    FROM read_parquet('parquet/movilidad/sitycleta.parquet')
    WHERE Latitud IS NOT NULL AND Longitud IS NOT NULL
),
-- Para cada estación Sitycleta, calcula la distancia mínima a una parada GTFS
-- Usa la fórmula haversine aproximada: 1 grado lat ~ 111320m, 1 grado lon ~ 111320*cos(lat)
-- Nota: DuckDB no tiene función ST_Distance en coordenadas geográficas sin extension
-- Así que usamos aproximación plana para distancias pequeñas (<5km)
station_distances AS (
    SELECT
        s.station_id,
        s.Nombre,
        s.Calle,
        s.Latitud,
        s.Longitud,
        min( -- Distancia euclídea aproximada en metros (válida para Canarias, lat ~28°)
            sqrt(
                POWER((s.Latitud - t.stop_lat) * 111320.0, 2) +
                POWER((s.Longitud - t.stop_lon) * 111320.0 * COS(RADIANS(28.1)), 2)
            )
        ) AS distancia_minima_m,
        arg_min(t.stop_name,
            sqrt(
                POWER((s.Latitud - t.stop_lat) * 111320.0, 2) +
                POWER((s.Longitud - t.stop_lon) * 111320.0 * COS(RADIANS(28.1)), 2)
            )
        ) AS parada_mas_cercana
    FROM sitycleta s
    CROSS JOIN stops t
    GROUP BY s.station_id, s.Nombre, s.Calle, s.Latitud, s.Longitud
)
SELECT
    station_id,
    Nombre,
    Calle,
    round(distancia_minima_m, 0) AS distancia_parada_mas_cercana_m,
    CASE
        WHEN distancia_minima_m <= 100 THEN 'Muy cercana (<100m)'
        WHEN distancia_minima_m <= 300 THEN 'Cercana (100-300m)'
        WHEN distancia_minima_m <= 500 THEN 'A distancia (300-500m)'
        ELSE 'Lejana (>500m)'
    END AS categoria_acceso,
    parada_mas_cercana
FROM station_distances
ORDER BY distancia_minima_m;
