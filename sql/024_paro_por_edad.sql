-- Perfil del desempleo por grupo de edad en LPGC (2008-2026)
-- El paro está envejeciendo: los mayores de 50 concentran cada vez más paro
-- Fuente: ISTAC Paro Registrado por sexo y edad

WITH por_edad AS (
    SELECT
        CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\d{4})', 1) AS INTEGER) AS anno,
        CASE EDAD_CODE
            WHEN 'Y_LT20' THEN '< 20'
            WHEN 'Y20T24' THEN '20-24'
            WHEN 'Y25T29' THEN '25-29'
            WHEN 'Y30T34' THEN '30-34'
            WHEN 'Y35T39' THEN '35-39'
            WHEN 'Y40T44' THEN '40-44'
            WHEN 'Y45T49' THEN '45-49'
            WHEN 'Y50T54' THEN '50-54'
            WHEN 'Y55T59' THEN '55-59'
            WHEN 'Y_GE60' THEN '60+'
        END AS grupo_edad,
        AVG(OBS_VALUE) AS paro_medio
    FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
    WHERE SEXO_CODE = '_T'
      AND TERRITORIO_CODE = 35016
      AND EDAD_CODE != '_T'
    GROUP BY anno, EDAD_CODE
)
SELECT anno, grupo_edad,
       round(paro_medio, 0) AS paro_medio,
       -- Variación desde 2008
       FIRST(paro_medio) OVER (PARTITION BY grupo_edad ORDER BY anno) AS paro_2008,
       round((paro_medio - FIRST(paro_medio) OVER (PARTITION BY grupo_edad ORDER BY anno)) * 100.0 /
             NULLIF(FIRST(paro_medio) OVER (PARTITION BY grupo_edad ORDER BY anno), 0), 1) AS var_desde_2008_pct
FROM por_edad
WHERE anno IN (2008, 2013, 2019, 2024)
ORDER BY anno, paro_medio DESC;
