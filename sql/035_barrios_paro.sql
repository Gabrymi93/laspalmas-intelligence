-- Barrios con mayor y menor tasa de paro (2024)
SELECT label as barrio, pact_t as poblacion_activa, tpar_t as tasa_paro
FROM read_parquet('parquet/geografia/dim_barrios.parquet')
WHERE tpar_t IS NOT NULL
ORDER BY tpar_t DESC
LIMIT 10;
