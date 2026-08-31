"""
Movilidad — GTFS, Sitycleta, accidentes de tráfico.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    accidentes_evolucion, accidentes_franja_horaria,
    gtfs_paradas_map, sitycleta_stations,
)

st.set_page_config(page_title="Movilidad — LPGC", page_icon="🚌", layout="wide")
st.title("🚌 Movilidad")

# ── Datos base ──────────────────────────────────────────────────────────
df_acc = accidentes_evolucion()
total_acc = int(df_acc["accidentes"].sum())
media_her = round(df_acc["media_heridos"].mean(), 2)

df_paradas = gtfs_paradas_map()
n_paradas = len(df_paradas)

df_sity = sitycleta_stations()
n_sity = len(df_sity)

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Accidentes totales", f"{total_acc:,}".replace(",", "."))
c2.metric("Media heridos/accidente", f"{media_her}")
c3.metric("Paradas GTFS", f"{n_paradas}")
c4.metric("Estaciones Sitycleta", f"{n_sity}")

st.divider()

# ── Evolución accidentes (dual axis) ────────────────────────────────────
st.subheader("📉 Evolución de accidentes de tráfico")
st.warning("⚠️ Datos incompletos: solo disponibles 1998-1999, 2002-2005 y 2012-2014. Faltan 2000-2001, 2006-2011 y 2015-2016.")

fig1 = go.Figure()
fig1.add_trace(go.Bar(x=df_acc["year"], y=df_acc["accidentes"], name="Accidentes",
                      marker_color="#3b82f6", yaxis="y"))
fig1.add_trace(go.Scatter(x=df_acc["year"], y=df_acc["media_heridos"], name="Media heridos",
                          mode="lines+markers", line=dict(color="#ef4444", width=3), yaxis="y2"))
fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                   xaxis_title="Año",
                   yaxis=dict(title="Accidentes", side="left"),
                   yaxis2=dict(title="Media heridos", side="right", overlaying="y", range=[0, 1]),
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig1, width="stretch")

# ── Franja horaria ──────────────────────────────────────────────────────

# Evolución accidentes: dual axis con barras + línea de severidad
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("⏰ Accidentes por franja horaria")
    df_frag = accidentes_franja_horaria()
    fig2 = px.bar(df_frag, x="franja", y="accidentes", color="media_heridos",
                  color_continuous_scale=["#22c55e", "#eab308", "#ef4444"],
                  labels={"franja": "Franja horaria", "accidentes": "Accidentes",
                          "media_heridos": "Media heridos"})
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
    st.plotly_chart(fig2, width="stretch")

with col_b:
    st.subheader("📊 Distribución por franja")
    total_frag = df_frag["accidentes"].sum()
    df_frag["pct"] = round(df_frag["accidentes"] * 100 / total_frag, 1)
    fig3 = go.Figure(go.Pie(labels=df_frag["franja"], values=df_frag["accidentes"],
                            hole=0.4, marker_colors=["#22c55e", "#eab308", "#f59e0b", "#ef4444"]))
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350, showlegend=True,
                       legend=dict(orientation="h", yanchor="bottom", y=-0.1))
    st.plotly_chart(fig3, width="stretch")

# ── Mapa paradas GTFS + Sitycleta ───────────────────────────────────────
st.subheader("🗺️ Mapa de transporte público")

# Centro Las Palmas
lat_center, lon_center = 28.1235, -15.4363
m = folium.Map(location=[lat_center, lon_center], zoom_start=13, tiles="OpenStreetMap")

# Paradas GTFS (muestra aleatoria de 200 para rendimiento)
df_sample = df_paradas.sample(min(200, len(df_paradas)), random_state=42)
for _, row in df_sample.iterrows():
    folium.CircleMarker(
        location=[row["stop_lat"], row["stop_lon"]],
        radius=2, color="#3b82f6", fill=True, fill_opacity=0.6,
        popup=row["stop_name"]
    ).add_to(m)

# Sitycleta
for _, row in df_sity.iterrows():
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=f"🚲 {row['Nombre']}<br>{row['Calle']}",
        icon=folium.Icon(color="green", icon="bicycle", prefix="fa")
    ).add_to(m)

st_folium(m, width="stretch", height=500)

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: El 65% de los accidentes ocurre entre las 12:00 y 24:00h.
La franja nocturna (18-24h) tiene la media de heridos más alta (0.66).
La red GTFS cuenta con 644 paradas; Sitycleta tiene 11 estaciones como
complemento al transporte público.
""")
