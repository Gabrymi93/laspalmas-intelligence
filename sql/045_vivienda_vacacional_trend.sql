-- Evolución mensual de viviendas vacacionales en LPGC (2019-2026)
-- Fuente: ISTAC C00065A_000061
SELECT
    TIME_PERIOD_CODE as periodo,
    try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\\d{4})', 1) AS INTEGER) as anno,
    try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, 'M(\\d{2})', 1) AS INTEGER) as mes,
    round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_DISPONIBLES' THEN OBS_VALUE END)) as viviendas_disp,
    round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_RESERVADAS' THEN OBS_VALUE END)) as viviendas_reserv,
    round(avg(CASE WHEN MEDIDAS_CODE='PLAZAS_DISPONIBLES' THEN OBS_VALUE END)) as plazas_disp,
    round(avg(CASE WHEN MEDIDAS_CODE='ESTANCIA_MEDIA_VIVIENDA_VACACIONAL' THEN OBS_VALUE END), 2) as estancia_media,
    round(avg(CASE WHEN MEDIDAS_CODE='INGRESOS_TOTALES' THEN OBS_VALUE END), 0) as ingresos,
    round(avg(CASE WHEN MEDIDAS_CODE='TASA_VIVIENDA_RESERVADA' THEN OBS_VALUE END), 1) as tasa_reserva
FROM read_parquet('parquet/turismo/vivienda_vacacional_lpgc.parquet')
WHERE INTERVALOS_PLAZAS_CODE = '_T'
GROUP BY 1, 2, 3
ORDER BY 2, 3;
