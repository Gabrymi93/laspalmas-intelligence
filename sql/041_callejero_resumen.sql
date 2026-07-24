-- Resumen del callejero municipal de LPGC
-- 5.305 segmentos viales, 2.491 vías únicas
-- Fuente: ArcGIS REST API — sit.laspalmasgc.es (CALLEJERO.CA_V_TRA_TRAMOS)

SELECT 'TOTAL SEGMENTOS' AS seccion, CAST(count(*) AS VARCHAR) AS valor FROM read_parquet('parquet/geografia/callejero_lpgc.parquet')
UNION ALL
SELECT 'VÍAS ÚNICAS', CAST(count(DISTINCT via_completa) AS VARCHAR) FROM read_parquet('parquet/geografia/callejero_lpgc.parquet')
UNION ALL
SELECT 'LONGITUD TOTAL (km)', CAST(round(sum(longitud_m) / 1000, 1) AS VARCHAR) FROM read_parquet('parquet/geografia/callejero_lpgc.parquet')
UNION ALL
SELECT 'TIPO + FRECUENTE', tipo_via || ' (' || CAST(cnt AS VARCHAR) || ')' FROM (
    SELECT tipo_via, count(*) AS cnt FROM read_parquet('parquet/geografia/callejero_lpgc.parquet')
    GROUP BY tipo_via ORDER BY cnt DESC LIMIT 1
)
UNION ALL
SELECT 'VIA + LARGA', via_completa FROM read_parquet('parquet/geografia/callejero_lpgc.parquet')
ORDER BY 1;
