# Arquitectura del repositorio

## Estructura de directorios

```
laspalmas-intelligence/
├── bin/                # utilidades (runner queries, status, validación, csv2parquet)
├── ingest/             # scripts de descarga por fuente (ETL)
├── parquet/            # datos limpios en Parquet
│   ├── poblacion/      # población + indicadores + secciones
│   ├── empleo/         # paro registrado sexo/edad + sexo/ocupación
│   ├── economia/       # renta bruta, empresas, autónomos
│   ├── movilidad/      # GTFS + atestados policía + sitycleta
│   ├── turismo/        # ocupación, pernoctaciones, gasto
│   ├── urbanismo/      # PGO + planes parciales (GeoParquet)
│   └── geografia/      # distritos, barrios, secciones, callejero
├── sql/                # 41 consultas DuckDB (#001-#041)
├── meta/
│   ├── catalog.json    # inventario completo de fuentes y datasets
│   └── next-session.md # plan para próxima sesión
├── docs/               # documentación
├── explore/            # informes de análisis
├── .venv/              # entorno virtual Python
├── requirements.txt    # dependencias
├── requirements.lock   # versiones precisas
└── Makefile            # automatización
```

## Makefile

| Comando | Acción |
|---------|--------|
| `make venv` | Crear .venv e instalar dependencias |
| `make refresh` | Descargar y actualizar todos los datasets |
| `make validate` | Validar integridad de datasets (rows, año) |
| `make queries` | Ejecutar las 41 consultas SQL |
| `make status` | Resumen de datasets y filas |
| `make all` | venv + refresh + validate + queries + status |

Cada dataset tiene su propio target (e.g. `make population`, `make empresas`, `make callejero`).

## DuckDB

- **Versión**: 1.5.4 via Python (package pip).
- **Spatial extension**: `ST_Transform` requiere dos SRID + `ST_FlipCoordinates`:
  ```sql
  ST_Transform(ST_FlipCoordinates(geom), 'EPSG:4326', 'EPSG:32628')
  ```
- El CLI `duckdb` del sistema puede estar en otra versión. Usar siempre `.venv/bin/python3`.

## CI/CD

| Workflow | Trigger | Acción |
|----------|---------|--------|
| `ci.yml` | push/PR a main | make validate + make queries |
| `refresh.yml` | Lun 6:00 + manual | make refresh → make validate → make queries → commit si hay cambios |

### Refresh semanal
1. Descarga datos de ISTAC, SITCAN, Ayto LPGC
2. Valida integridad (make validate)
3. Ejecuta queries (make queries)
4. Si hay cambios, commit automatico
5. Si falla, crea issue de notificación

Si algún target falla, el workflow falla (no `|| echo`). No hay commit parcial.
