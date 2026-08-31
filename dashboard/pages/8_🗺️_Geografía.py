"""
Geografía — Mapas interactivos, callejero, comparativa de distritos.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    distritos_resumen, callejero_stats, query as dq,
)

st.set_page_config(page_title="Geografía — LPGC", page_icon="🗺️", layout="wide")
st.title("🗺️ Geografía")

# ── Datos base ──────────────────────────────────────────────────────────
df_dist = distritos_resumen()
n_distritos = len(df_dist)
n_barrios = int(dq("""SELECT count(*) as v FROM read_parquet('parquet/geografia/barrios_lpgc.parquet')""")["v"].iloc[0])
n_secciones = int(dq("""SELECT count(*) as v FROM read_parquet('parquet/poblacion/poblacion_secciones.parquet')""")["v"].iloc[0])
df_calle = callejero_stats()
n_calles = int(df_calle["vie"].sum())

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Distritos", f"{n_distritos}")
c2.metric("Barrios", f"{n_barrios}")
c3.metric("Secciones censales", f"{n_secciones}")
c4.metric("Vías en callejero", f"{n_calles:,}".replace(",", "."))

st.divider()

# ── Mapa distritos (choropleth via GeoJSON) ─────────────────────────────
st.subheader("🏙️ Mapa de distritos — Tasa de paro")

df_geo = dq("""SELECT label, tpar_t, pact_t, tsal_t,
    ST_AsGeoJSON(geometry) as geojson
    FROM read_parquet('parquet/geografia/distritos_lpgc.parquet')""")

def get_color(tpar):
    if tpar > 24: return "#ef4444"
    if tpar > 21: return "#f59e0b"
    if tpar > 19: return "#eab308"
    return "#22c55e"

m = folium.Map(location=[28.12, -15.43], zoom_start=12, tiles="OpenStreetMap")

for _, row in df_geo.iterrows():
    gj = json.loads(row["geojson"])
    folium.GeoJson(
        gj,
        style_function=lambda feature, tpar=row["tpar_t"]: {
            "fillColor": get_color(tpar),
            "color": get_color(tpar),
            "weight": 2,
            "fillOpacity": 0.4,
        },
        popup=folium.Popup(
            f"<b>{row['label']}</b><br>"
            f"Paro: {row['tpar_t']}%<br>"
            f"Activos: {row['pact_t']:,}<br>"
            f"Salarización: {row['tsal_t']}%",
            max_width=250
        )
    ).add_to(m)

# Leyenda
legend_html = """<div style="position:fixed;bottom:30px;left:30px;z-index:1000;
    background:rgba(255,255,255,0.92);padding:10px;border-radius:5px;color:#111;font-size:12px;border:1px solid #ccc;"><b>Tasa de paro</b><br>
    <span style="color:#22c55e;">■</span> &lt;19%<br>
    <span style="color:#eab308;">■</span> 19-21%<br>
    <span style="color:#f59e0b;">■</span> 21-24%<br>
    <span style="color:#ef4444;">■</span> &gt;24%</div>"""
m.get_root().html.add_child(folium.Element(legend_html))

st_folium(m, width="stretch", height=500)

# ── Fila 2: Radar comparativo + Tabla ───────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 Comparativa de distritos")
    cats = ["Paro (%)", "Activos (×1000)", "Salarización (%)"]
    fig = go.Figure()
    for _, row in df_dist.iterrows():
        nombre = row["distrito"].split(" - ")[0]
        fig.add_trace(go.Scatterpolar(
            r=[row["tasa_paro"], row["activos"] / 1000, row["tasa_salarizacion"]],
            theta=cats, fill="toself", name=nombre
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)),
                      margin=dict(l=0, r=0, t=30, b=0), height=400,
                      legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig, width="stretch")

with col_b:
    st.subheader("📋 Detalle por distrito")
    st.dataframe(
        df_dist.rename(columns={
            "distrito": "Distrito", "activos": "Activos",
            "tasa_paro": "Paro (%)", "tasa_salarizacion": "Salarización (%)",
        }), width="stretch", hide_index=True
    )

# ── Estadísticas callejero ──────────────────────────────────────────────
st.subheader("🛣️ Estadísticas del callejero municipal")

col_c, col_d = st.columns(2)

with col_c:
    df_top = df_calle.head(10)
    fig2 = px.bar(df_top, x="vie", y="tipo_via", orientation="h",
                  text_auto=True, color="lunghezza_totale",
                  color_continuous_scale=["#0ea5e9", "#3b82f6"],
                  labels={"vie": "Número de vías", "tipo_via": "", "lunghezza_totale": "Longitud total (m)"})
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                       coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig2, width="stretch")

with col_d:
    fig3 = px.bar(df_top, x="lunghezza_totale", y="tipo_via", orientation="h",
                  text_auto=".0f", color="lunghezza_totale",
                  color_continuous_scale=["#22c55e", "#16a34a"],
                  labels={"lunghezza_totale": "Longitud (m)", "tipo_via": "", "vie": "Vías"})
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                       coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, width="stretch")

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: El Distrito 02 tiene la tasa de paro más baja (16.8%) y alta salarización
(84.7%), mientras el Distrito 01 concentra el mayor desempleo (25.1%). El callejero cuenta
con 4.478 calles que suman 538 km — la red viaria más extensa es la de tipo CALLE.
""")
