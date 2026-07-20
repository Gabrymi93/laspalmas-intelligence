-- Pernottamenti mensili Gran Canaria 2010-2026
SELECT anno, mese, OBS_VALUE AS pernottamenti
FROM read_parquet('parquet/turismo/pernottamenti_gran_canaria.parquet')
ORDER BY anno, mese
