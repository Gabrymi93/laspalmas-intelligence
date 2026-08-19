-- Sensores propios del proyecto Gemelo Digital: medias por mercado y sensor
-- Nota: lecturas crudas del sensor (valores sin factor de escala)

SELECT mercado,
       label AS sensor,
       count(*) AS lecturas,
       round(avg(pm2_5), 1) AS pm25_media,
       round(avg(pm_10), 1) AS pm10_media,
       round(avg(co2), 0) AS co2_media,
       round(avg(temperatura), 1) AS temperatura_media,
       round(avg(humedad), 1) AS humedad_media
FROM read_parquet('parquet/ambiente/calidad_aire_gemelo.parquet')
GROUP BY 1, 2
ORDER BY 1, 2;
