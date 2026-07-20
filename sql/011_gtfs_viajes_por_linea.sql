-- Viajes por linea
SELECT r.route_short_name AS linea,
       r.route_long_name AS nombre,
       count(DISTINCT t.trip_id) AS viajes,
       count(DISTINCT st.stop_id) AS paradas
FROM read_parquet('parquet/movilidad/gtfs_routes.parquet') r
JOIN read_parquet('parquet/movilidad/gtfs_trips.parquet') t ON r.route_id = CAST(t.route_id AS VARCHAR)
JOIN read_parquet('parquet/movilidad/gtfs_stop_times.parquet') st ON t.trip_id = st.trip_id
GROUP BY r.route_id, r.route_short_name, r.route_long_name
ORDER BY try_cast(r.route_short_name AS INTEGER), r.route_short_name
