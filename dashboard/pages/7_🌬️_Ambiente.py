"""
Ambiente — Calidad del aire, estaciones, sensores Gemelo Digital.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import folium
from streamlit_folium import st_folium
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    calidad_aire_estaciones, calidad_aire_stazioni_geo, calidad_aire_gemelo,
)

st.set_page_config(page_title="Ambiente — LPGC", page_icon="🌬️", layout="wide")
st.title("🌬️ Ambiente — Calidad del aire")

# ── Datos base ──────────────────────────────────────────────────────────
df_est = calidad_aire_estaciones()
df_geo = calidad_aire_stazioni_geo()
df_gem = calidad_aire_gemelo()

n_estaciones = len(df_geo)
total_lecturas = int(df_est["lecturas"].sum())
n_parametros = len(df_est["parametro"].unique())
n_sensores = len(df_gem)

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Estaciones Gob. Canarias", f"{n_estaciones}")
c2.metric("Lecturas totales", f"{total_lecturas:,}".replace(",", "."))
c3.metric("Parámetros medidos", f"{n_parametros}")
c4.metric("Sensores Gemelo Digital", f"{n_sensores}")

st.divider()

# ── Mapa estaciones ─────────────────────────────────────────────────────
st.subheader("🗺️ Mapa de estaciones de calidad del aire")

# Mapear estaciones geo con sus parámetros
est_params = df_est.groupby("estacion").agg(
    params=("parametro", lambda x: "<br>• ".join(x)),
    lecturas=("lecturas", "sum")
).reset_index()

df_map = df_geo.merge(est_params, left_on="nombre", right_on="estacion", how="left")

m = folium.Map(location=[28.11, -15.43], zoom_start=12, tiles="OpenStreetMap")

for _, row in df_map.iterrows():
    popup_html = f"""<b>{row['nombre']}</b><br>
        Lecturas: {row.get('lecturas', 0):,}<br>
        Parámetros:<br>• {row.get('params', 'N/A')}"""
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color="blue", icon="cloud", prefix="fa")
    ).add_to(m)

st_folium(m, width="stretch", height=400)

# ── Tabla resumen ───────────────────────────────────────────────────────
st.subheader("📋 Resumen por estación y parámetro")

# Pivotear para mejor visualización
df_pivot = df_est.pivot_table(index="estacion", columns="parametro",
                              values="media", aggfunc="first")
# Renombrar columnas para que sean más legibles
rename_cols = {
    "Concentracion de NO2": "NO₂",
    "Concentracion de O3": "O₃",
    "Concentracion de SO2": "SO₂",
    "Concentracion de PM2,5": "PM2.5",
    "Particulas en suspension < 10um": "PM10",
    "Particulas en suspension < 2,5um": "PM2.5 (2,5)",
    "Particulas en suspension < 2,5um": "PM2.5 (2,5)",
}
df_pivot.columns = [rename_cols.get(c, c) for c in df_pivot.columns]

df_pivot.index.name = "Estación"

colores = {
    "NO₂": "#3b82f6",
    "O₃": "#8b5cf6",
    "SO₂": "#f59e0b",
    "PM2.5": "#ef4444",
    "PM2.5 (2,5)": "#ef4444",
    "PM10": "#f97316",
}

fig = go.Figure()
for col in df_pivot.columns:
    if col in ["PM2.5", "PM2.5 (2,5)"]:
        continue  # skip duplicate
    fig.add_trace(go.Bar(name=col, x=df_pivot.index, y=df_pivot[col],
                         marker_color=colores.get(col, "#6b7280")))

fig.update_layout(barmode="group", margin=dict(l=0, r=0, t=10, b=0), height=400,
                  yaxis_title="Concentración media",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, width="stretch")

# ── Gemelo Digital: sensores propios ────────────────────────────────────
st.subheader("🏙️ Sensores Gemelo Digital — Mercados")

col_a, col_b = st.columns(2)

with col_a:
    # PM2.5 por sensor
    fig2 = px.bar(df_gem, x="sensor", y="pm25", color="mercado",
                  color_discrete_map={"MercadoCentral": "#3b82f6", "MercadoPuerto": "#22c55e"},
                  labels={"sensor": "Sensor", "pm25": "PM2.5 (media)", "mercado": "Mercado"})
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
    st.plotly_chart(fig2, width="stretch")

with col_b:
    # CO₂ por sensor
    fig3 = px.bar(df_gem, x="sensor", y="co2", color="mercado",
                  color_discrete_map={"MercadoCentral": "#3b82f6", "MercadoPuerto": "#22c55e"},
                  labels={"sensor": "Sensor", "co2": "CO₂ (media)", "mercado": "Mercado"})
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
    st.plotly_chart(fig3, width="stretch")

# ── Temperatura y humedad ───────────────────────────────────────────────
st.subheader("🌡️ Temperatura y humedad por sensor")

df_gem_long = df_gem.melt(id_vars=["mercado", "sensor"],
                           value_vars=["temp", "pm25"],
                           var_name="variable", value_name="valor")

fig4 = px.bar(df_gem, x="sensor", y="temp", color="mercado",
              color_discrete_map={"MercadoCentral": "#ef4444", "MercadoPuerto": "#f59e0b"},
              labels={"sensor": "Sensor", "temp": "Temperatura (°C)", "mercado": "Mercado"})
fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
st.plotly_chart(fig4, width="stretch")

# ── Tabla detallada sensores ────────────────────────────────────────────
st.subheader("📊 Detalle sensores Gemelo Digital")
st.dataframe(
    df_gem.rename(columns={
        "mercado": "Mercado", "sensor": "Sensor", "lecturas": "Lecturas",
        "pm25": "PM2.5", "co2": "CO₂", "temp": "Temp (°C)"
    }), width="stretch", hide_index=True
)

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: Las 4 estaciones del Gobierno de Canarias miden NO₂, O₃, SO₂, PM10 y PM2.5.
El Mercado Central registra el PM2.5 más bajo (8.83) entre las estaciones del Gobierno.
Los sensores propios del Gemelo Digital muestran valores crudos elevados (sin corrección de escala).
""")
