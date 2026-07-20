-- Brecha de género en el desempleo de LPGC (2008-2026)
-- Evolución del paro femenino vs masculino
-- Fuente: ISTAC Paro Registrado por sexo y edad

WITH por_sexo AS (
    SELECT 
        CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\d{4})', 1) AS INTEGER) AS anno,
        SEXO_CODE,
        CASE SEXO_CODE
            WHEN 'M' THEN 'Hombres'
            WHEN 'F' THEN 'Mujeres'
        END AS sexo,
        AVG(OBS_VALUE) AS paro_medio_mensual
    FROM read_parquet('parquet/empleo/paro_sexo_edad.parquet')
    WHERE EDAD_CODE = '_T' 
      AND TERRITORIO_CODE = 35016
      AND SEXO_CODE IN ('M', 'F')
    GROUP BY anno, SEXO_CODE
)
SELECT 
    a.anno,
    round(a.paro_medio_mensual, 0) AS paro_masculino,
    round(b.paro_medio_mensual, 0) AS paro_femenino,
    round(a.paro_medio_mensual + b.paro_medio_mensual, 0) AS paro_total,
    -- Diferencia absoluta (mujeres - hombres)
    round(b.paro_medio_mensual - a.paro_medio_mensual, 0) AS brecha_absoluta,
    -- Ratio femenino / masculino
    round(b.paro_medio_mensual * 100.0 / NULLIF(a.paro_medio_mensual, 0), 1) AS indice_paridad,
    -- % de mujeres sobre el total de parados
    round(b.paro_medio_mensual * 100.0 / (a.paro_medio_mensual + b.paro_medio_mensual), 1) AS pct_mujeres
FROM por_sexo a
JOIN por_sexo b ON a.anno = b.anno AND a.SEXO_CODE = 'M' AND b.SEXO_CODE = 'F'
ORDER BY a.anno;
