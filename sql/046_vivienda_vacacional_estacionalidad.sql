-- Perfil estacional de viviendas vacacionales (promedio 2019-2026)
-- Fuente: ISTAC C00065A_000061
WITH mensual AS (
    SELECT
        try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, 'M(\\d{2})', 1) AS INTEGER) as mes,
        try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\\d{4})', 1) AS INTEGER) as anno,
        round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_DISPONIBLES' THEN OBS_VALUE END)) as viviendas_disp,
        round(avg(CASE WHEN MEDIDAS_CODE='TASA_VIVIENDA_RESERVADA' THEN OBS_VALUE END), 1) as tasa_reserva,
        round(avg(CASE WHEN MEDIDAS_CODE='INGRESOS_TOTALES' THEN OBS_VALUE END), 0) as ingresos
    FROM read_parquet('parquet/turismo/vivienda_vacacional_lpgc.parquet')
    WHERE INTERVALOS_PLAZAS_CODE = '_T'
    GROUP BY 1, 2
)
SELECT
    mes,
    CASE mes
        WHEN 1 THEN 'Ene' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
        WHEN 4 THEN 'Abr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
        WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago' WHEN 9 THEN 'Sep'
        WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dic'
    END as mes_label,
    round(avg(viviendas_disp)) as viviendas_media,
    round(avg(tasa_reserva), 1) as reserva_media,
    round(avg(ingresos), 0) as ingresos_media
FROM mensual
GROUP BY mes
ORDER BY mes;
