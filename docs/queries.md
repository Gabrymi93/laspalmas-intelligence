# Consultas SQL (44)

Todas las consultas están en `sql/` y se ejecutan con `make queries`.

## Población (001-004)
| # | Archivo | Descripción |
|---|---------|-------------|
| 001 | `001_poblacion_trend.sql` | Tendencia población LPGC 1986-2025 |
| 002 | `002_poblacion_sexo.sql` | Composición por sexo |
| 003 | `003_poblacion_extranjeros.sql` | Población extranjera |
| 004 | `004_estructura_edad.sql` | Estructura de edad (jóvenes/adultos/mayores) |

## Empleo (005-008, 013, 024-025)
| # | Archivo | Descripción |
|---|---------|-------------|
| 005 | `005_paro_tendencia.sql` | Tendencia mensual del paro 2008-2026 |
| 006 | `006_paro_sexo.sql` | Paro por sexo |
| 007 | `007_paro_edad.sql` | Paro por edad |
| 008 | `008_paro_anual.sql` | Paro anual |
| 013 | `013_paro_juvenil_barrio.sql` | Tasa de paro juvenil (16-24) por barrio |
| 024 | `024_paro_por_edad.sql` | Perfil del desempleo por grupo de edad |
| 025 | `025_paro_por_sexo.sql` | Brecha de género en el desempleo |

## Movilidad (009-012, 016-018)
| # | Archivo | Descripción |
|---|---------|-------------|
| 009 | `009_incidentes_horario.sql` | Patrones temporales de accidentes (hora/día/mes/año) |
| 010 | `010_gtfs_rutas.sql` | Líneas de guaguas |
| 011 | `011_gtfs_viajes_por_linea.sql` | Viajes por línea |
| 012 | `012_gtfs_servicio_calendario.sql` | Calendario de servicio GTFS |
| 016 | `016_incidentes_tipo.sql` | Accidentes por tipo de colisión y evolución |
| 017 | `017_gtfs_sitycleta.sql` | Complementariedad guaguas × Sitycleta |
| 018 | `018_incidentes_paro_temporal.sql` | Comparación temporal accidentes ↔ desempleo |

## Turismo (020-023)
| # | Archivo | Descripción |
|---|---------|-------------|
| 020 | `020_turismo_occupazione_hotel.sql` | Ocupación hotelera LPGC por categoría |
| 021 | `021_turismo_pernottamenti.sql` | Pernoctaciones mensuales Gran Canaria |
| 022 | `022_turismo_spesa_paesi.sql` | Gasto turístico por país de origen |
| 023 | `023_estacionalidad_turistica.sql` | Estacionalidad turística (perfil mensual) |

## Economía (015, 019, 026-029, 034, 039)
| # | Archivo | Descripción |
|---|---------|-------------|
| 015 | `015_verde_vs_renta.sql` | Renta, verde y mercado laboral por distrito |
| 019 | `019_empresas_evolucion.sql` | Evolución tejido empresarial por tamaño |
| 026 | `026_empresas_vs_paro.sql` | Micro-empresas ↔ desempleo |
| 027 | `027_autonomos_trend.sql` | Evolución autónomos LPGC (2010-2026) |
| 028 | `028_demanda_coworking.sql` | Demanda potencial coworking |
| 029 | `029_autonomos_sectores.sql` | Distribución sectorial autónomos |
| 034 | `034_renta_por_distrito.sql` | Renta por distrito (composición por fuente) |
| 039 | `039_paro_vs_renta.sql` | Paro vs renta por distrito |

## Urbanismo (030-033, 037-038)
| # | Archivo | Descripción |
|---|---------|-------------|
| 030 | `030_urbanismo_pgo_zonificacion.sql` | Zonificación del PGO |
| 031 | `031_urbanismo_catalogo.sql` | Catálogo de protección |
| 032 | `032_urbanismo_resumen.sql` | Resumen de planeamiento |
| 033 | `033_verde_pro_capite.sql` | Espacio verde pro-capite LPGC |
| 037 | `037_verde_por_barrio.sql` | Espacios verdes por barrio |
| 038 | `038_verde_por_distrito.sql` | Espacios verdes por distrito |

## Geografía (035-036, 041)
| # | Archivo | Descripción |
|---|---------|-------------|
| 035 | `035_barrios_paro.sql` | Barrios con mayor/menor tasa de paro |
| 036 | `036_distritos_laborales.sql` | Comparativa laboral entre distritos |
| 041 | `041_callejero_resumen.sql` | Resumen del callejero municipal |

## Seguridad (040)
| # | Archivo | Descripción |
|---|---------|-------------|
| 040 | `040_atestados_severidad.sql` | Evolución de la severidad de accidentes |

## Ambiente (042-044)
| # | Archivo | Descripción |
|---|---------|-------------|
| 042 | `042_calidad_aire_resumen.sql` | Resumen de sensores de calidad del aire (Gemelo Digital) |
| 043 | `043_calidad_aire_estaciones.sql` | Media y última lectura por estación y parámetro (Gob. de Canarias) |
| 044 | `044_calidad_aire_gemelo_mercados.sql` | Medias por mercado y sensor (sensores propios) |
