# Contribuir

Gracias por tu interés en **laspalmas-intelligence**. Este es un proyecto OSINT ciudadano, abierto a contribuciones que mejoren la calidad, cobertura o análisis de los datos.

## Cómo contribuir

### Reportar problemas
- Abre un [issue](https://github.com/Gabrymi93/laspalmas-intelligence/issues) describiendo el problema.
- Incluye: fuente del error, query SQL si aplica, y comportamiento esperado vs real.

### Sugerir fuentes o datasets
- Abre un issue con la etiqueta `nueva-fuente`.
- Indica: URL, formato, frecuencia de actualización, licencia y granularidad.
- Si ya existe un script de ingest similar, menciona la referencia.

### Añadir una query
1. Crea un archivo `sql/XXX_descripcion.sql` (usa el número disponible más cercano).
2. Sigue el estilo existente:
   - Comentario inicial en español describiendo la query
   - Código SQL legible, con CTEs cuando sea necesario
   - Sin columnas duplicadas ni SELECT *
3. Verifica que funciona con `make queries`.

### Añadir un dataset
1. Crea el script de ingest en `ingest/` (ver ejemplos existentes).
2. Los datos limpios van en `parquet/<dominio>/`.
3. Actualiza `meta/catalog.json` con el nuevo dataset.
4. Añade la query(ies) de análisis en `sql/`.
5. Verifica con `make queries && make status`.

### Modificar el pipeline
- Los scripts en `ingest/` son ETL independientes para cada fuente.
- Los scripts en `bin/` son utilidades transversales (runner queries, status).
- No uses pandas para transformaciones pesadas; prefiere DuckDB directo.

## Estilo

| Elemento | Regla |
|----------|-------|
| **Código** | en inglés (nombres de variables, funciones) |
| **Documentación** | en español (comentarios SQL, README, issues) |
| **SQL** | CTEs descriptivas, `JOIN` explícito, alias claros |
| **Python** | `snake_case`, type hints, docstrings |
| **Makefile** | targets con dependencias vía `.venv/bin/python3` |

## Entorno de desarrollo

```bash
make venv          # crear .venv e instalar dependencias
make refresh       # descargar datos (requiere internet)
make queries       # validar queries (35, 0 errores esperados)
make status        # resumen de datasets
```

## Licencia

Al contribuir, aceptas que tus contribuciones se distribuyan bajo la licencia **MIT** del proyecto.
