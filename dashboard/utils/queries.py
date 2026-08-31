"""Centralized DuckDB queries for the dashboard."""
import os
import duckdb
import pandas as pd
from streamlit import cache_data

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _p(path: str) -> str:
    return os.path.join(PROJECT_ROOT, path)

def _connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    return con

@cache_data(ttl=3600)
def query(sql: str) -> pd.DataFrame:
    con = _connect()
    try:
        return con.execute(sql).fetchdf()
    finally:
        con.close()

# ── KPI ─────────────────────────────────────────────────────────────────

def kpi_poblacion() -> int:
    df = query(f"""SELECT value as v FROM read_parquet('{_p('parquet/poblacion/poblacion_serie_historica.parquet')}')
        WHERE measure_code='POBLACION' ORDER BY year DESC LIMIT 1""")
    return int(df["v"].iloc[0])

def kpi_paro() -> int:
    df = query(f"""SELECT round(avg(OBS_VALUE)) as v FROM read_parquet('{_p('parquet/empleo/paro_sexo_edad.parquet')}')
        WHERE EDAD_CODE='_T' AND SEXO_CODE='_T' AND TERRITORIO_CODE=35016
        AND TIME_PERIOD_CODE LIKE (SELECT max(substr(TIME_PERIOD_CODE,1,4))||'%' FROM read_parquet('{_p('parquet/empleo/paro_sexo_edad.parquet')}') WHERE EDAD_CODE='_T')""")
    return int(df["v"].iloc[0])

def kpi_empresas() -> int:
    df = query(f"""SELECT round(avg(valor)) as v FROM read_parquet('{_p('parquet/economia/empresas_lpgc.parquet')}')
        WHERE estrato_code='_T' AND valor>0
        AND year=(SELECT max(year) FROM read_parquet('{_p('parquet/economia/empresas_lpgc.parquet')}') WHERE estrato_code='_T')""")
    return int(df["v"].iloc[0])

def kpi_ocupacion_hotelera() -> float:
    df = query(f"""SELECT round(avg(CASE WHEN \"ALOJAMIENTO_TURISTICO_CATEGORIA#es\"='Total' THEN OBS_VALUE END),1) as v
        FROM read_parquet('{_p('parquet/turismo/occupazione_hotel_lpgc.parquet')}')
        GROUP BY anno ORDER BY anno DESC LIMIT 1""")
    return float(df["v"].iloc[0])

# ── Overview ─────────────────────────────────────────────────────────────

def poblacion_trend() -> pd.DataFrame:
    return query(f"""SELECT year, round(avg(value)) as poblacion
        FROM read_parquet('{_p('parquet/poblacion/poblacion_serie_historica.parquet')}')
        WHERE measure_code='POBLACION' AND year>=1990 GROUP BY year ORDER BY year""")

def paro_trend_total() -> pd.DataFrame:
    return query(f"""SELECT CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE,'(\\d{{4}})',1) AS INTEGER) as anno,
        round(avg(CASE WHEN SEXO_CODE='_T' THEN OBS_VALUE END)) as paro_total,
        round(avg(CASE WHEN SEXO_CODE='M' THEN OBS_VALUE END)) as paro_hombres,
        round(avg(CASE WHEN SEXO_CODE='F' THEN OBS_VALUE END)) as paro_mujeres
        FROM read_parquet('{_p('parquet/empleo/paro_sexo_edad.parquet')}')
        WHERE EDAD_CODE='_T' AND TERRITORIO_CODE=35016 GROUP BY anno ORDER BY anno""")

def paro_por_distrito() -> pd.DataFrame:
    return query(f"""SELECT label as distrito, tpar_t as tasa_paro, pact_t as activos
        FROM read_parquet('{_p('parquet/geografia/dim_distritos.parquet')}') ORDER BY tpar_t DESC""")

# ── Demografía ───────────────────────────────────────────────────────────

def evolucion_estructura_edad() -> pd.DataFrame:
    return query(f"""SELECT date, poblacion_00a14, poblacion_15a64, poblacion_65mas, poblacion as total
        FROM read_parquet('{_p('parquet/poblacion/indicadores_demograficos.parquet')}')
        ORDER BY date""")

def envejecimiento_distritos() -> pd.DataFrame:
    return query(f"""SELECT label as distrito, pact_t_16a24 as jovenes, pact_t_55mas as mayores_55, pact_t as activos,
        round(pact_t_55mas*100.0/NULLIF(pact_t,0),1) as pct_55mas,
        round(pact_t_16a24*100.0/NULLIF(pact_t,0),1) as pct_jovenes,
        round(pact_t_55mas*100.0/NULLIF(pact_t_16a24,0),0) as indice_envejecimiento
        FROM read_parquet('{_p('parquet/geografia/distritos_lpgc.parquet')}') ORDER BY indice_envejecimiento DESC""")

def edad_media_secciones() -> float:
    df = query(f"""SELECT round(avg(poblacion_edad_media),1) as v
        FROM read_parquet('{_p('parquet/poblacion/poblacion_secciones.parquet')}')""")
    return float(df["v"].iloc[0])


def secciones_censales_map() -> pd.DataFrame:
    return query(f"""SELECT geocode, seccion_code, poblacion, poblacion_edad_media,
        poblacion_65mas, poblacion_00a14, superficie,
        round(poblacion/NULLIF(superficie,0),0) as densidad,
        round(poblacion_65mas*100.0/NULLIF(poblacion,0),1) as pct_mayores
        FROM read_parquet('{_p('parquet/poblacion/poblacion_secciones.parquet')}')""")

# ── Empleo ───────────────────────────────────────────────────────────────

def paro_mensual_sexo() -> pd.DataFrame:
    return query(f"""SELECT TIME_PERIOD_CODE as periodo,
        CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE,'(\\d{{4}})',1) AS INTEGER) as anno,
        round(avg(CASE WHEN SEXO_CODE='M' THEN OBS_VALUE END)) as hombres,
        round(avg(CASE WHEN SEXO_CODE='F' THEN OBS_VALUE END)) as mujeres,
        round(avg(CASE WHEN SEXO_CODE='_T' THEN OBS_VALUE END)) as total
        FROM read_parquet('{_p('parquet/empleo/paro_sexo_edad.parquet')}')
        WHERE EDAD_CODE='_T' AND TERRITORIO_CODE=35016 GROUP BY periodo ORDER BY periodo""")

def paro_por_edad_anios() -> pd.DataFrame:
    return query(f"""SELECT CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE,'(\\d{{4}})',1) AS INTEGER) as anno,
        EDAD_CODE as edad_code, \"EDAD#es\" as edad_label, round(avg(OBS_VALUE)) as paro_medio
        FROM read_parquet('{_p('parquet/empleo/paro_sexo_edad.parquet')}')
        WHERE SEXO_CODE='_T' AND EDAD_CODE!='_T' AND TERRITORIO_CODE=35016
        AND CAST(REGEXP_EXTRACT(TIME_PERIOD_CODE,'(\\d{{4}})',1) AS INTEGER) IN (2008,2013,2024)
        GROUP BY 1,2,3 ORDER BY 1,2""")

def paro_juvenil_barrios() -> pd.DataFrame:
    return query(f"""SELECT label as barrio, pact_t as activos,
        tpar_t as tasa_paro_general,
        round(ppar_t_16a24*100.0/NULLIF(pact_t_16a24,0),1) as tasa_paro_juvenil
        FROM read_parquet('{_p('parquet/geografia/barrios_lpgc.parquet')}')
        WHERE pact_t_16a24>0 AND ppar_t_16a24 IS NOT NULL ORDER BY tasa_paro_juvenil DESC""")

def barrios_paro_top10() -> pd.DataFrame:
    return query(f"""SELECT label as barrio, tpar_t as tasa_paro, pact_t as activos
        FROM read_parquet('{_p('parquet/geografia/dim_barrios.parquet')}')
        WHERE tpar_t IS NOT NULL ORDER BY tpar_t DESC LIMIT 10""")

# ── Economía ─────────────────────────────────────────────────────────────

def renta_por_distrito() -> pd.DataFrame:
    return query(f"""SELECT h.distrito_label as distrito,
        round(avg(CASE WHEN r.medida_code='SUELDOS_SALARIOS' THEN r.valor END),1) as sueldos,
        round(avg(CASE WHEN r.medida_code='PENSIONES' THEN r.valor END),1) as pensiones,
        round(avg(CASE WHEN r.medida_code='PRESTACIONES_DESEMPLEO' THEN r.valor END),1) as desempleo,
        round(avg(CASE WHEN r.medida_code='OTROS_INGRESOS' THEN r.valor END),1) as otros
        FROM read_parquet('{_p('parquet/economia/renta_secciones_lpgc.parquet')}') r
        JOIN read_parquet('{_p('parquet/geografia/dim_hierarchy.parquet')}') h ON r.seccion_code=h.seccion_code
        WHERE r.year=2023 GROUP BY h.distrito_label ORDER BY h.distrito_label""")

def empresas_evolucion() -> pd.DataFrame:
    return query(f"""SELECT year, estrato_label, round(avg(valor)) as media
        FROM read_parquet('{_p('parquet/economia/empresas_lpgc.parquet')}')
        WHERE estrato_code!='_T' AND valor IS NOT NULL AND valor>0
        GROUP BY year, estrato_label ORDER BY year, estrato_label""")

def autonomos_trend() -> pd.DataFrame:
    return query(f"""SELECT year, round(avg(valor)) as autonomos
        FROM read_parquet('{_p('parquet/economia/autonomos_lpgc.parquet')}')
        WHERE year IS NOT NULL GROUP BY year ORDER BY year""")

def demanda_coworking() -> pd.DataFrame:
    return query(f"""WITH a AS (SELECT year,round(avg(valor),0) AS autonomos FROM read_parquet('{_p('parquet/economia/autonomos_lpgc.parquet')}') GROUP BY year),
        m AS (SELECT year,round(avg(valor),0) AS micro FROM read_parquet('{_p('parquet/economia/empresas_lpgc.parquet')}') WHERE estrato_code='1T9' AND valor>0 GROUP BY year),
        p AS (SELECT year,value AS pop FROM read_parquet('{_p('parquet/poblacion/poblacion_serie_historica.parquet')}') WHERE measure_code='POBLACION')
        SELECT a.year, a.autonomos, m.micro, a.autonomos+m.micro as demanda, p.pop,
        round((a.autonomos+m.micro)*1000.0/p.pop,1) as por_mil_hab
        FROM a JOIN m ON a.year=m.year JOIN p ON a.year=p.year ORDER BY a.year""")

def autonomos_sectores() -> pd.DataFrame:
    return query(f"""SELECT sector, round(avg(valor)) as media
        FROM read_parquet('{_p('parquet/economia/autonomos_sectores_lpgc.parquet')}')
        WHERE SITUACION_EMPLEO_CODE='EMPLEOS_CUENTA_PROPIA' AND SEXO_CODE='_T'
        GROUP BY sector ORDER BY media DESC LIMIT 15""")

# ── Turismo ──────────────────────────────────────────────────────────────

def ocupacion_hotelera() -> pd.DataFrame:
    return query(f"""SELECT anno,
        round(avg(CASE WHEN \"ALOJAMIENTO_TURISTICO_CATEGORIA#es\"='1, 2 y 3 Estrellas' THEN OBS_VALUE END),1) as bajas,
        round(avg(CASE WHEN \"ALOJAMIENTO_TURISTICO_CATEGORIA#es\"='4 y 5 Estrellas' THEN OBS_VALUE END),1) as altas,
        round(avg(CASE WHEN \"ALOJAMIENTO_TURISTICO_CATEGORIA#es\"='Total' THEN OBS_VALUE END),1) as total
        FROM read_parquet('{_p('parquet/turismo/occupazione_hotel_lpgc.parquet')}')
        GROUP BY anno ORDER BY anno""")

def pernottamenti_mensili() -> pd.DataFrame:
    return query(f"""SELECT anno, mese, round(OBS_VALUE) as pernoctaciones
        FROM read_parquet('{_p('parquet/turismo/pernottamenti_gran_canaria.parquet')}')
        WHERE anno>=2010 ORDER BY anno, mese""")

def spesa_per_paese() -> pd.DataFrame:
    return query(f"""SELECT paese, round(sum(OBS_VALUE)/1e9,2) as miliardi_eur
        FROM read_parquet('{_p('parquet/turismo/spesa_turistica_paesi.parquet')}')
        WHERE anno=(SELECT max(anno) FROM read_parquet('{_p('parquet/turismo/spesa_turistica_paesi.parquet')}')) AND paese!='Total'
        GROUP BY paese ORDER BY miliardi_eur DESC""")


# ── Vivienda Vacacional ─────────────────────────────────────────────────

def vivienda_vacacional_trend() -> pd.DataFrame:
    return query(f"""SELECT TIME_PERIOD_CODE as periodo,
        try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, '(\\d{{4}})', 1) AS INTEGER) as anno,
        try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE, 'M(\\d{{2}})', 1) AS INTEGER) as mes,
        round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_DISPONIBLES' THEN OBS_VALUE END)) as viviendas_disp,
        round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_RESERVADAS' THEN OBS_VALUE END)) as viviendas_reserv,
        round(avg(CASE WHEN MEDIDAS_CODE='PLAZAS_DISPONIBLES' THEN OBS_VALUE END)) as plazas_disp,
        round(avg(CASE WHEN MEDIDAS_CODE='ESTANCIA_MEDIA_VIVIENDA_VACACIONAL' THEN OBS_VALUE END), 2) as estancia_media,
        round(avg(CASE WHEN MEDIDAS_CODE='INGRESOS_TOTALES' THEN OBS_VALUE END), 0) as ingresos,
        round(avg(CASE WHEN MEDIDAS_CODE='TASA_VIVIENDA_RESERVADA' THEN OBS_VALUE END), 1) as tasa_reserva
        FROM read_parquet('{_p('parquet/turismo/vivienda_vacacional_lpgc.parquet')}')
        WHERE INTERVALOS_PLAZAS_CODE='_T' AND TIME_PERIOD_CODE IS NOT NULL AND TIME_PERIOD_CODE!=''
        GROUP BY 1,2,3 ORDER BY 2,3""")


def vivienda_vacacional_estacionalidad() -> pd.DataFrame:
    return query(f"""WITH m AS (
        SELECT try_cast(REGEXP_EXTRACT(TIME_PERIOD_CODE,'M(\\d{{2}})',1) AS INTEGER) as mes,
            round(avg(CASE WHEN MEDIDAS_CODE='VIVIENDAS_VACACIONALES_DISPONIBLES' THEN OBS_VALUE END)) as viviendas_disp,
            round(avg(CASE WHEN MEDIDAS_CODE='TASA_VIVIENDA_RESERVADA' THEN OBS_VALUE END),1) as tasa_reserva,
            round(avg(CASE WHEN MEDIDAS_CODE='INGRESOS_TOTALES' THEN OBS_VALUE END),0) as ingresos
        FROM read_parquet('{_p('parquet/turismo/vivienda_vacacional_lpgc.parquet')}')
        WHERE INTERVALOS_PLAZAS_CODE='_T' GROUP BY 1)
        SELECT mes,
            CASE mes WHEN 1 THEN 'Ene' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
            WHEN 4 THEN 'Abr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
            WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago' WHEN 9 THEN 'Sep'
            WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dic' END as mes_label,
            round(avg(viviendas_disp)) as viviendas_media,
            round(avg(tasa_reserva),1) as reserva_media,
            round(avg(ingresos),0) as ingresos_media
        FROM m GROUP BY 1 ORDER BY 1""")


# ── Movilidad ────────────────────────────────────────────────────────────

def accidentes_evolucion() -> pd.DataFrame:
    return query(f"""SELECT year, count(*) as accidentes, round(avg(HERIDOS),2) as media_heridos
        FROM read_parquet('{_p('parquet/movilidad/atestados_acc.parquet')}')
        WHERE HERIDOS IS NOT NULL GROUP BY year ORDER BY year""")

def accidentes_franja_horaria() -> pd.DataFrame:
    return query(f"""SELECT CASE
        WHEN h BETWEEN 0 AND 5 THEN '00-06 madrugada'
        WHEN h BETWEEN 6 AND 11 THEN '06-12 manana'
        WHEN h BETWEEN 12 AND 17 THEN '12-18 tarde'
        WHEN h BETWEEN 18 AND 23 THEN '18-24 noche'
        END AS franja, count(*) as accidentes, round(avg(HERIDOS),2) as media_heridos
        FROM (SELECT DILIG,HERIDOS,CAST(REGEXP_EXTRACT(HORA,'(\\d{{2}})',1) AS INTEGER) AS h
        FROM read_parquet('{_p('parquet/movilidad/atestados_acc.parquet')}') WHERE year>=2000 AND HORA IS NOT NULL)
        GROUP BY 1 ORDER BY 2 DESC""")

def gtfs_paradas_map() -> pd.DataFrame:
    return query(f"""SELECT stop_name, stop_lat, stop_lon FROM read_parquet('{_p('parquet/movilidad/gtfs_stops.parquet')}')""")

def sitycleta_stations() -> pd.DataFrame:
    return query(f"""SELECT Nombre, Calle, Latitud, Longitud FROM read_parquet('{_p('parquet/movilidad/sitycleta.parquet')}')""")

# ── Ambiente ─────────────────────────────────────────────────────────────

def calidad_aire_estaciones() -> pd.DataFrame:
    return query(f"""SELECT nombre_estacion AS estacion, nombre_parametro AS parametro,
        count(*) AS lecturas,
        round(avg(CAST(valor_numerico AS DOUBLE)) FILTER (WHERE valor_texto<>'No disponible'),2) AS media,
        max(datetime) AS ultima_lectura
        FROM read_parquet('{_p('parquet/ambiente/calidad_aire_estaciones.parquet')}')
        GROUP BY 1,2 ORDER BY 1,2""")

def calidad_aire_stazioni_geo() -> pd.DataFrame:
    return query(f"""SELECT * FROM read_parquet('{_p('parquet/ambiente/calidad_aire_estaciones_geo.parquet')}')""")

def calidad_aire_gemelo() -> pd.DataFrame:
    return query(f"""SELECT mercado, label as sensor, count(*) as lecturas,
        round(avg(pm2_5),1) as pm25, round(avg(pm_10),1) as pm10,
        round(avg(co2),0) as co2, round(avg(temperatura),1) as temp
        FROM read_parquet('{_p('parquet/ambiente/calidad_aire_gemelo.parquet')}')
        GROUP BY 1,2 ORDER BY 1,2""")

# ── Geografía ────────────────────────────────────────────────────────────

def distritos_resumen() -> pd.DataFrame:
    return query(f"""SELECT label as distrito, pact_t as activos, tpar_t as tasa_paro, tsal_t as tasa_salarizacion
        FROM read_parquet('{_p('parquet/geografia/dim_distritos.parquet')}')""")

def callejero_stats() -> pd.DataFrame:
    return query(f"""SELECT tipo_via, count(*) as vie, round(sum(longitud_m)) as lunghezza_totale
        FROM read_parquet('{_p('parquet/geografia/callejero_lpgc.parquet')}')
        GROUP BY tipo_via ORDER BY vie DESC""")
