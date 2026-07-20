-- Calendarios de servicio
SELECT service_id,
       monday, tuesday, wednesday, thursday, friday, saturday, sunday,
       start_date, end_date
FROM read_parquet('parquet/movilidad/gtfs_calendar.parquet')
ORDER BY service_id
