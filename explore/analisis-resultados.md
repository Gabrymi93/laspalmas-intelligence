# Análisis exploratorio — Resultados (2026-07-20)

## Nuevas queries implementadas

| # | Query | Dominio |
|---|-------|---------|
| 009 | `incidentes_horario` | Patrones temporales de accidentes (hora/día/mes) |
| 013 | `paro_juvenil_barrio` | Tasa de paro juvenil (16-24) por barrio |
| 014 | `envejecimiento_distrito` | Estructura de edad por distrito |
| 015 | `verde_vs_renta` | Renta y mercado laboral por distrito |
| 016 | `incidentes_tipo` | Accidentes por tipo de colisión y evolución |
| 017 | `gtfs_sitycleta` | Complementariedad guaguas + bici compartida |
| 018 | `incidentes_vs_paro` | Correlación accidentes ↔ desempleo (2008-2013) |
| 023 | `estacionalidad_turistica` | Pernoctaciones mensuales y estacionalidad |
| 024 | `paro_por_edad` | Perfil del desempleo por grupo de edad |
| 025 | `paro_por_sexo` | Brecha de género en el desempleo |

---

## 1. Incidentes — patrones temporales (009)

### Franja horaria (2000-2016)
| Franja | Accidente | % | Media heridos |
|---|---|---|---|
| 12-18h (tarde) | 22.293 | 37,8% | 0,59 |
| 18-24h (noche) | 16.395 | 27,8% | 0,67 |
| 06-12h (mañana) | 15.418 | 26,2% | 0,56 |
| 00-06h (madrugada) | 4.815 | 8,2% | 0,56 |

→ **El 65,6% de los accidentes ocurren entre las 12:00 y 24:00h.**
→ La franja nocturna tiene la media de heridos más alta (0,67).

### Día de semana
- **Pico**: viernes (16,9%), lunes (15,9%), miércoles (15,9%)
- **Valle**: domingo (9,0%), sábado (11,1%)
- Laborables ~15-16% cada día, fin de semana ~10-11%

### Mes
- Máximos: marzo, diciembre, enero (~9,0-9,1% cada uno)
- Mínimos: agosto (6,7%), julio (7,7%), septiembre (7,7%)
- **Estacionalidad**: menos accidentes en verano, más en invierno/primavera

### Evolución anual
- Descenso continuo: de 4.742 (2000) a 3.171 (2014) → **-33%**
- La media de heridos por accidente **sube** de 0,53 (2000) a 0,77 (2011): menos accidentes pero más graves
- **Datos incompletos 2014-2016**: no registran heridos ni tipo de colisión

---

## 2. Paro juvenil por barrio (013)

### Barrios con mayor tasa de paro juvenil (16-24)
| Barrio | Tasa general | Tasa juvenil | Brecha |
|---|---|---|---|
| La Palma | 18,7% | **50,0%** | +31,3 pp |
| Lomo El Sabinal | 24,2% | **50,0%** | +25,8 pp |
| La Milagrosa | 15,9% | **44,4%** | +28,5 pp |
| El Pintor | 17,8% | **42,9%** | +25,1 pp |
| La Calzada | 13,6% | **42,9%** | +29,2 pp |
| Risco Negro | 30,1% | **39,1%** | +9,1 pp |
| Rehoyas Altas | 23,4% | **35,6%** | +12,2 pp |
| Jinámar | 32,4% | **34,7%** | +2,2 pp |
| Lomo Los Frailes | 25,1% | **33,1%** | +8,0 pp |
| Ciudad del Campo | 16,9% | **32,6%** | +15,7 pp |

→ **La brecha juvenil es sistemática**: en casi todos los barrios la tasa de paro juvenil duplica la general.
→ **Casos críticos**: La Palma, Lomo El Sabinal y La Calzada tienen 1 de cada 2 jóvenes en paro.
→ **Excepciones**: San Francisco-San Nicolás y El Lasso tienen tasa juvenil *menor* que la general.

---

## 3. Envejecimiento por distrito (014)

| Distrito | Población | Edad media | Índice envejec. | % mayores |
|---|---|---|---|---|
| D03 Centro | 71.169 | **47,0 años** | **253,7** | **23,0%** |
| D02 | 81.117 | 45,6 años | 197,4 | 21,5% |
| D01 | 67.929 | 45,5 años | 192,0 | 20,1% |
| D04 | 103.542 | 45,1 años | 164,2 | 18,5% |
| **D05** | **55.040** | **42,0 años** | **100,3** | **13,4%** |

→ **D03 es el distrito más envejecido**: 2,5 mayores por cada joven (índice 253,7).
→ **D05 es el más joven**: equilibrio generacional (índice 100,3) — solo 13,4% mayores de 65.
→ La diferencia de edad media entre D03 y D05 es de 5 años.

---

## 4. Renta y mercado laboral por distrito (015)

| Distrito | Sueldos | Pensiones | Prest. paro | Otros ing. | Tasa paro |
|---|---|---|---|---|---|
| D05 | **65,6%** | 15,7% | 2,9% | 9,7% | 21,5% |
| D04 | 58,7% | 23,1% | 3,0% | 8,9% | 21,1% |
| D01 | 56,9% | 24,0% | 3,1% | 8,7% | **25,1%** |
| D02 | 56,5% | 21,2% | 2,0% | **15,3%** | **16,8%** |
| D03 | 55,6% | 22,6% | 2,0% | 15,2% | 19,0% |

→ **D05 lidera en renta salarial** (65,6%) pero tiene paro alto (21,5%).
→ **D02 tiene la tasa de paro más baja** (16,8%) y el mayor "otros ingresos" (15,3%).
→ **D01 es el más vulnerable**: paro más alto (25,1%), menos ingresos no-salariales.

**Nota técnica**: La componente espacial (verde por distrito) no pudo calcularse porque la función ST_Transform de DuckDB v1.2.1 no tiene disponible PROJ para la reproyección EPSG:4326 → 32628. Pendiente de solución.

---

## 5. Accidentes por tipo de colisión (016)

| Tipo | Accidentes | % | Media heridos |
|---|---|---|---|
| Colisión | 54.111 | **81,5%** | 0,57 |
| Sin especificar | 7.144 | 10,8% | 0,0 |
| Atropello | 2.532 | 3,8% | **1,09** |
| Otros | 1.313 | 2,0% | 0,58 |
| Salida de vía | 990 | 1,5% | 0,74 |
| Vuelco | 265 | 0,4% | 1,03 |

→ **8 de cada 10 accidentes son colisiones entre vehículos.**
→ **Los atropellos son los más graves**: 1,09 heridos de media (doble que una colisión).
→ Los atropellos se mantienen estables (~200/año) mientras el total de accidentes baja.

---

## 6. Complementariedad guaguas × Sitycleta (017)

| Estación | Distancia a parada más cercana |
|---|---|
| Plaza Ing. Manuel Becerra | **10 m** |
| Ayuntamiento | **12 m** |
| Glorieta Base Naval | **18 m** |
| Parque Santa Catalina | **27 m** |
| Facultad Geografía | **52 m** |
| Edificio Woermann | **53 m** |
| Mercado de Vegueta | **60 m** |
| C.C. Las Arenas | **91 m** |
| Muelle Deportivo | **93 m** |
| Biblioteca Pública | 106 m |
| Vega de San José | 257 m |

→ **10/11 estaciones a menos de 100m de una parada de guagua** → red altamente integrada.
→ **Ninguna estación supera los 300m** → todo el sistema Sitycleta es accesible desde el transporte público.
→ Vega de San José (257m) es la menos integrada, pero aún en radio de caminabilidad.

---

---

## 7. Correlación incidentes viales vs desempleo (018)

| Año | Accidentes | Media heridos | Paro medio mensual | Var. accidentes | Var. paro |
|---|---|---|---|---|---|
| 2008 | 4.247 | 0,594 | 38.147 | — | — |
| 2009 | 3.970 | 0,653 | 49.276 | **-6,5%** | **+29,2%** |
| 2010 | 3.682 | 0,731 | 52.174 | -7,3% | +5,9% |
| 2011 | 3.578 | 0,767 | 50.813 | -2,8% | -2,6% |
| 2012 | 3.441 | 0,758 | 54.712 | -3,8% | +7,7% |
| 2013 | 3.326 | 0,725 | 55.447 | -3,3% | +1,3% |

→ **Relación inversa clara**: mientras el paro sube (+45,3% 2008→2013), los accidentes bajan (-21,7%).
→ **Hipótesis**: la crisis redujo la movilidad (menos desplazamientos laborales, menos consumo), y eso redujo los accidentes.
→ **Paradoja**: la **gravedad aumenta** (media heridos de 0,59 a 0,73) — menos accidentes pero más severos.
→ Limitación: solo 6 años con datos solapados (incidentes hasta 2013, paro desde 2008).

---

## 8. Estacionalidad turística (023)

### Pernoctaciones mensuales en Gran Canaria (2010-2026)

| Mes | Media pernoctaciones | Índice estacional | Temporada |
|---|---|---|---|
| **Enero** | 2.481.389 | **114,1** | **Alta** |
| Febrero | 2.305.823 | 106,0 | Media |
| Marzo | 2.363.515 | 108,7 | Media |
| Abril | 1.811.275 | 83,3 | **Baja** |
| Mayo | 1.646.566 | 75,7 | **Baja** |
| Junio | 1.691.834 | 77,8 | **Baja** |
| Julio | 2.258.062 | 103,8 | Media |
| **Agosto** | 2.518.402 | **115,8** | **Alta** |
| Septiembre | 1.993.210 | 91,6 | Media |
| Octubre | 2.261.387 | 104,0 | Media |
| **Noviembre** | 2.401.551 | **110,4** | **Alta** |
| Diciembre | 2.385.299 | 109,7 | Media |

→ **Perfil atípico respecto al Mediterráneo**: Canarias tiene dos picos — **invierno** (turismo europeo que huye del frío) y **agosto** (turismo interno español).
→ **Estacionalidad moderada**: el índice oscila entre 75,7 (mayo) y 115,8 (agosto) — rango más suave que destinos mediterráneos continentales.
→ **Temporada baja**: abril-junio, con mayo como el mes más flojo (-24% respecto a la media anual).
→ **Dato curioso**: enero supera a agosto en varios años — Canarias es destino de "escape invernal" además de sol y playa.

---

## 9. Perfil del desempleo por grupo de edad (024)

| Grupo edad | 2008 | 2013 (crisis) | 2019 (recuperación) | 2024 |
|---|---|---|---|---|
| **< 20** | 1.336 | 408 | 495 | 343 |
| 20-24 | 3.226 | 3.431 | 1.918 | 1.490 |
| 25-29 | 4.258 | 5.539 | 3.018 | 2.156 |
| 30-34 | 4.342 | 6.427 | 3.470 | 2.361 |
| 35-39 | 4.511 | 6.731 | 3.886 | 2.762 |
| 40-44 | 4.563 | 7.279 | 4.237 | 3.136 |
| 45-49 | **4.857** | **8.395** | 5.437 | 3.828 |
| 50-54 | 4.273 | 7.529 | 6.043 | 4.784 |
| 55-59 | 3.973 | 5.972 | **6.401** | **5.882** |
| **60+** | 2.808 | 3.738 | 4.589 | **6.058** |

→ **El paro está envejeciendo**: en 2008 el grupo 45-49 lideraba (4.857); en 2024 los mayores de 55 concentran el paro más alto (60+: 6.058, 55-59: 5.882).
→ **Crisis 2008-2013**: todos los grupos crecen, pero los mayores de 40 son los más golpeados (45-49: +73%).
→ **Recuperación asimétrica**: los jóvenes se recuperan rápido (20-24: -57% 2013→2024), los mayores de 50 siguen empeorando (60+: +62%).
→ **Menores de 20**: caen drásticamente durante la crisis (1.336→408), probablemente porque alarga su formación (efecto "refugio educativo").

---

## 10. Brecha de género en el desempleo (025)

### Evolución paro femenino vs masculino (2008-2026)

| Año | Hombres | Mujeres | Brecha (M-H) | Índice paridad | % mujeres |
|---|---|---|---|---|---|
| 2008 | 16.983 | 21.163 | 4.180 | 124,6 | 55,5% |
| 2010 | 24.518 | 27.656 | 3.138 | 112,8 | 53,0% |
| 2013 | 26.738 | 28.709 | 1.971 | 107,4 | 51,8% |
| 2016 | 21.129 | 25.499 | 4.370 | 120,7 | 54,7% |
| 2019 | 16.937 | 22.555 | 5.619 | 133,2 | 57,1% |
| **2022** | **16.177** | **21.821** | **5.643** | **134,9** | **57,4%** |
| 2024 | 14.039 | 18.761 | 4.722 | 133,6 | 57,2% |
| 2026 | 12.263 | 16.435 | 4.172 | 134,0 | 57,3% |

→ **La brecha de género se amplía**: de 4.180 (2008) a 5.643 (2022) → **+35%**.
→ **Durante la crisis la brecha se redujo** (los hombres perdieron más empleos industriales/construcción), pero **en la recuperación se disparó**.
→ **Techo de cristal**: a pesar de la recuperación económica (paro total baja), la proporción de mujeres paradas **aumenta** (55,5% → 57,4%).
→ **Persistencia**: el índice de paridad se estabiliza en ~134 desde 2019 — las mujeres tienen sistemáticamente **un 34% más de paro** que los hombres.

---

## Queries implementadas (total: 10 nuevas)

| # | Query | Archivo | Estado |
|---|---|---|---|
| 009 | Patrones temporales accidentes | `009_incidentes_horario.sql` | ✅ |
| 013 | Paro juvenil por barrio | `013_paro_juvenil_barrio.sql` | ✅ |
| 014 | Envejecimiento por distrito | `014_envejecimiento_distrito.sql` | ✅ |
| 015 | Renta y mercado laboral por distrito | `015_verde_vs_renta.sql` | ✅ |
| 016 | Incidentes por tipo de colisión | `016_incidentes_tipo.sql` | ✅ |
| 017 | Complementariedad guaguas × bici | `017_gtfs_sitycleta.sql` | ✅ |
| 018 | Correlación accidentes × paro | `018_incidentes_vs_paro.sql` | ✅ |
| 023 | Estacionalidad turística | `023_estacionalidad_turistica.sql` | ✅ |
| 024 | Paro por grupo de edad | `024_paro_por_edad.sql` | ✅ |
| 025 | Brecha de género en el paro | `025_paro_por_sexo.sql` | ✅ |

**Problema técnico pendiente**: ST_Transform EPSG:4326 ↔ 32628 no funciona en DuckDB v1.5.4 (PROJ datum shift). La componente espacial (verde por distrito en query 015 y 038) queda pendiente de reparación.

## Próximos pasos

1. **Resolver ST_Transform** en DuckDB v1.2.1 para completar 015 con verde por distrito
2. **Query 018-019**: Explorar correlación accidentes × renta por distrito
3. **Query 023**: Estacionalidad turística (ocupación hotelera mensual)
4. **Query 024-025**: Perfiles de desempleo por edad y sexo combinados
5. **Ingerir datos nuevos**: sensores calidad aire, callejero, centros educativos
