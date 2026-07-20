-- Lineas de guaguas municipales
SELECT route_id, route_short_name, route_long_name, route_type
FROM read_parquet('parquet/movilidad/gtfs_routes.parquet')
ORDER BY route_short_name
