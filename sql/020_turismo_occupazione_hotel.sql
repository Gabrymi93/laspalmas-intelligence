-- Occupazione hotel LPGC 2009-2026 per categoria
SELECT anno,
       categoria,
       round(OBS_VALUE, 1) AS occupazione_pct
FROM read_parquet('parquet/turismo/occupazione_hotel_lpgc.parquet')
WHERE categoria = 'Total'
ORDER BY anno
