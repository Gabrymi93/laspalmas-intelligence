"""
Las Palmas de Gran Canaria — Intelligence Dashboard
Punto de entrada para la app multi-página de Streamlit.
"""
import streamlit as st

st.set_page_config(
    page_title="LPGC Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.success("Selecciona una página de arriba ☝️")

st.title("🏙️ Las Palmas de Gran Canaria — Intelligence Dashboard")

st.markdown("""
Bienvenido a la dashboard interactiva de **laspalmas-intelligence**.

Repositorio OSINT que centraliza datos HVD (High Value Dataset) de
**Las Palmas de Gran Canaria** de fuentes oficiales: ISTAC, Ayuntamiento LPGC,
SITCAN, Eurostat.

### 📊 Dominios disponibles

| Página | Contenido |
|--------|-----------|
| 👥 **Demografía** | Población, envejecimiento, extranjeros |
| 💼 **Empleo** | Paro por sexo/edad/barrio, brecha de género |
| 💰 **Economía** | Renta por distrito, empresas, autónomos, coworking |
| 🏨 **Turismo** | Ocupación hotelera, pernoctaciones, gasto por país |
| 🚌 **Movilidad** | GTFS, Sitycleta, accidentes de tráfico |
| 🌬️ **Ambiente** | Calidad del aire, sensores Gemelo Digital |
| 🗺️ **Geografía** | Mapas interactivos, callejero |

### 📈 Datos actualizados
- **29 datasets** en Parquet (~570K registros)
- **44 consultas SQL** ejecutadas vía DuckDB
- Refresh semanal automático vía GitHub Actions
""")
