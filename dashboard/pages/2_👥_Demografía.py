"""
Demografía — Estructura de población, envejecimiento, extranjeros.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    evolucion_estructura_edad, envejecimiento_distritos, edad_media_secciones,
)

st.set_page_config(page_title="Demografía — LPGC", page_icon="👥", layout="wide")
st.title("👥 Demografía")

# ── KPIs ────────────────────────────────────────────────────────────────
df_edad = evolucion_estructura_edad()
ultima = df_edad.iloc[-1]
primera = df_edad.iloc[0]

mayores = int(ultima["poblacion_65mas"])
jovenes = int(ultima["poblacion_00a14"])
total = int(ultima["total"])
var_mayores = round((mayores - int(primera["poblacion_65mas"])) * 100 / int(primera["poblacion_65mas"]), 1)
var_jovenes = round((jovenes - int(primera["poblacion_00a14"])) * 100 / int(primera["poblacion_00a14"]), 1)

edad_media = edad_media_secciones()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Población total", f"{total:,}".replace(",", "."))
c2.metric("Mayores de 65", f"{mayores:,}".replace(",", "."), f"{var_mayores:+.1f}% desde 2008")
c3.metric("Menores de 15", f"{jovenes:,}".replace(",", "."), f"{var_jovenes:+.1f}% desde 2008")
c4.metric("Edad media", f"{edad_media}")

st.divider()

# ── Evolución estructura de edad (stacked area) ──────────────────────────
st.subheader("📊 Evolución de la estructura de edad (2008 → 2022)")

df_pct = df_edad.copy()
df_pct["% 0-14"] = round(df_pct["poblacion_00a14"] * 100 / df_pct["total"], 1)
df_pct["% 15-64"] = round(df_pct["poblacion_15a64"] * 100 / df_pct["total"], 1)
df_pct["% 65+"] = round(df_pct["poblacion_65mas"] * 100 / df_pct["total"], 1)
df_pct["año"] = df_pct["date"].str[:4].astype(int)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pct["año"], y=df_pct["% 65+"], name="65+ años",
                         fill="tozeroy", line=dict(color="#ef4444"), stackgroup="one"))
fig.add_trace(go.Scatter(x=df_pct["año"], y=df_pct["% 15-64"], name="15-64 años",
                         fill="tonexty", line=dict(color="#3b82f6"), stackgroup="one"))
fig.add_trace(go.Scatter(x=df_pct["año"], y=df_pct["% 0-14"], name="0-14 años",
                         fill="tonexty", line=dict(color="#22c55e"), stackgroup="one"))
fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                  xaxis_title="Año", yaxis_title="% de población",
                  yaxis=dict(range=[0, 100]),
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, width="stretch")

# ── Envejecimiento por distrito ─────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏙️ Envejecimiento por distrito")
    df_evc = envejecimiento_distritos()
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_evc["pct_55mas"], y=df_evc["distrito"], name=">55 años",
                          orientation="h", marker_color="#ef4444"))
    fig2.add_trace(go.Bar(x=df_evc["pct_jovenes"], y=df_evc["distrito"], name="16-24 años",
                          orientation="h", marker_color="#3b82f6"))
    fig2.update_layout(barmode="group", margin=dict(l=0, r=0, t=10, b=0), height=350,
                       xaxis_title="% sobre activos", legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig2, width="stretch")

with col_b:
    st.subheader("📈 Índice de envejecimiento")
    st.markdown("> **Mayores de 55 / Jóvenes de 16-24** — Un índice alto indica población activa más envejecida.")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=df_evc["distrito"], y=df_evc["indice_envejecimiento"],
                          marker_color=["#ef4444" if v > 400 else "#eab308" if v > 300 else "#22c55e"
                                        for v in df_evc["indice_envejecimiento"]]))
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350,
                       yaxis_title="Índice (mayores_55 / jóvenes_16-24)", xaxis_tickangle=-15)
    st.plotly_chart(fig3, width="stretch")

# ── Tabla resumen ───────────────────────────────────────────────────────
st.subheader("📋 Detalle por distrito")
st.dataframe(
    df_evc.rename(columns={
        "distrito": "Distrito", "activos": "Activos",
        "pct_55mas": "% >55", "pct_jovenes": "% 16-24",
        "indice_envejecimiento": "Índice envej."
    }), width="stretch", hide_index=True
)

# ── Insight ─────────────────────────────────────────────────────────────
st.info(f"""
💡 **Insight clave**: Desde 2008, la población >65 ha crecido un **{var_mayores:+.1f}%** mientras
los menores de 15 han caído un **{var_jovenes:+.1f}%**. El Distrito 03 (centro) es el más envejecido
con un índice de {df_evc.iloc[0]['indice_envejecimiento']:.0f} — más de 5 personas >55 por cada joven de 16-24.
""")
