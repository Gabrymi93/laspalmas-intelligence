-- Comparativa laboral entre distritos (2022)
SELECT label as distrito, pact_t as activos, pocu_t as ocupados,
       ppar_t as parados, round(tpar_t, 1) as tasa_paro,
       round(tsal_t, 1) as tasa_salarizacion
FROM read_parquet('parquet/geografia/dim_distritos.parquet')
ORDER BY distrito_code;
