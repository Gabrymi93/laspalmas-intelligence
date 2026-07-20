-- Spesa turistica Canarias per paese 2010-2024
SELECT anno, paese, OBS_VALUE AS spesa_euros
FROM read_parquet('parquet/turismo/spesa_turistica_paesi.parquet')
WHERE anno = 2017
ORDER BY spesa_euros DESC
