# Cobertura de datos

| Dominio | Dataset | Registros | Período | Granularidad | Fuente |
|---------|---------|-----------|---------|-------------|--------|
| Población | Serie histórica | 114 | 1986-2025 | municipio | ISTAC |
| Demografía | Indicadores | 15 | 2008-2022 | municipio | ISTAC |
| Población | Por sección censal (edad, sexo, origen) | 275 | 2022 | sección | WFS ISTAC |
| Empleo | Paro por sexo/edad | 7.260 | 2008-03 → 2026-06 | municipio, mensual | ISTAC |
| Empleo | Paro por sexo/ocupación | 6.105 | 2011-02 → 2026-06 | municipio, mensual | ISTAC |
| Transporte | GTFS rutas | 47 | 2026 | línea | Ayto LPGC |
| Transporte | GTFS viajes | 6.250 | 2026 | viaje | Ayto LPGC |
| Transporte | GTFS horarios | 151.551 | 2026 | parada/viaje | Ayto LPGC |
| Transporte | GTFS calendario | 9 | 2015-2025 | servicio | Ayto LPGC |
| Transporte | Sitycleta bike stations | 11 | 2018 | estación | Ayto LPGC |
| Turismo | Ocupación hotelera | 45 | 2009-2023 | LPGC + categoría | ISTAC |
| Turismo | Pernoctaciones | 197 | 2010-2026 | Gran Canaria, mensual | ISTAC |
| Turismo | Gasto turístico | 96 | 2010-2017 | Canarias, por país | ISTAC |
| Economía | Renta bruta por municipio | 45 | 2015-2023 | LPGC por fuente | ISTAC |
| Economía | Renta bruta por sección censal | 12.395 | 2015-2023 | 281 secciones LPGC | ISTAC |
| Economía | Empresas por estrato asalariados | 605 | 2012-2026 | LPGC, mensual | ISTAC |
| Economía | Autónomos (cuenta propia) | 114 | 2011-2026 | LPGC, trimestral | ISTAC |
| Seguridad | Atestados accidentes | 76.178 | 1998-2016 | LPGC, calle | Ayto LPGC |
| Seguridad | Atestados heridos | 45.488 | 1998-2016 | LPGC, edad/sexo/gravedad | Ayto LPGC |
| Seguridad | Atestados vehículos | 148.650 | 1998-2016 | LPGC, marca/modelo | Ayto LPGC |
| Urbanismo | PGO Plan General | 6.608 | 2012 | polígono (ZUSO) | SITCAN |
| Urbanismo | PGO catalogación | 821 | 2012 | elemento protegido | SITCAN |
| Urbanismo | Planes parciales | 28 planes GIS | 1994-2024 | polígono (ZUSO) | SITCAN |
| Geografía | Distritos (geometría + indicadores) | 5 | 2022 | distrito | WFS ISTAC |
| Geografía | Barrios (geometría + indicadores) | 121 | 2024 | barrio | WFS ISTAC |
| Geografía | Secciones censales (geometría) | 275 | 2022 | sección | WFS ISTAC |
| Geografía | Callejero municipal | 5.305 | 2026 | segmento vial | Ayto LPGC |
| Ambiente | Calidad aire: sensores propios (mercados) | 7.725 | 2026-05 → 2026-07 | sensor, ~horario | Ayto LPGC |
| Ambiente | Calidad aire: estaciones Gob. de Canarias | 118.840 | 2025-07 → 2026-05 | estación × parámetro | Ayto LPGC |
| Ambiente | Ubicación estaciones calidad del aire | 4 | 2026 | estación (lat/lon) | Ayto LPGC |

**Total**: 29 datasets, ~570K registros.

> Nota: los valores numéricos son lecturas crudas del sensor (sin factor de escala, pueden incluir negativos).
