-- Occupazione hotel LPGC 2009-2026 per categoria
SELECT anno,
       "ALOJAMIENTO_TURISTICO_CATEGORIA#es" as categoria,
       round(OBS_VALUE, 1) AS occupazione_pct
FROM read_parquet('parquet/turismo/occupazione_hotel_lpgc.parquet')
WHERE "ALOJAMIENTO_TURISTICO_CATEGORIA#es" LIKE '%Total%'
ORDER BY anno
