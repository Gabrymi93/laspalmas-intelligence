-- Tasa de paro juvenil (16-24 años) por barrio en LPGC (2024)
-- Compara desempleo juvenil vs desempleo general por barrio
-- Fuente: ISTAC Indicadores laborales por barrios (WFS)

WITH juveniles AS (
    SELECT
        label AS barrio,
        pact_t AS activos_totales,
        pocu_t AS ocupados_totales,
        ppar_t AS parados_totales,
        tpar_t AS tasa_paro_general,
        -- Población activa juvenil (16-24) y parados juveniles
        pact_t_16a24 AS activos_16_24,
        ppar_t_16a24 AS parados_16_24,
        -- Para cálculo de tasa juvenil
        CASE
            WHEN pact_t_16a24 IS NOT NULL AND pact_t_16a24 > 0
            THEN round(ppar_t_16a24 * 100.0 / pact_t_16a24, 1)
            ELSE NULL
        END AS tasa_paro_juvenil,
        -- Diferencia entre tasa general y juvenil
        pact_t_25a34 AS activos_25_34,
        ppar_t_25a34 AS parados_25_34,
        CASE
            WHEN pact_t_25a34 IS NOT NULL AND pact_t_25a34 > 0
            THEN round(ppar_t_25a34 * 100.0 / pact_t_25a34, 1)
            ELSE NULL
        END AS tasa_paro_25_34
    FROM read_parquet('parquet/geografia/barrios_lpgc.parquet')
    WHERE tpar_t IS NOT NULL AND pact_t_16a24 > 0
)

SELECT
    barrio,
    tasa_paro_general,
    tasa_paro_juvenil,
    round(tasa_paro_juvenil - tasa_paro_general, 1) AS brecha_juvenil,
    tasa_paro_25_34,
    activos_totales,
    activos_16_24,
    parados_16_24
FROM juveniles
ORDER BY tasa_paro_juvenil DESC NULLS LAST
LIMIT 30;
