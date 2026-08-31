"""
Resumen — Panel de KPIs
Vista panorámica de todos los dominios con KPIs y gráficos clave.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    kpi_poblacion, kpi_paro, kpi_empresas, kpi_ocupacion_hotelera,
    poblacion_trend, paro_trend_total, paro_por_distrito,
)

st.set_page_config(page_title="Resumen — LPGC", page_icon="🏙️", layout="wide")
st.title("🏙️ Resumen")

# ── Fila de KPIs ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Población", f"{kpi_poblacion():,}".replace(",", "."))
c2.metric("💼 Paro medio", f"{kpi_paro():,}".replace(",", "."))
c3.metric("🏢 Empresas", f"{kpi_empresas():,}".replace(",", "."))
c4.metric("🏨 Ocupación hotel", f"{kpi_ocupacion_hotelera()}%")

st.divider()

# ── Fila 1: Población + Evolución del paro ──────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Tendencia de población (1990 → 2025)")
    df_pop = poblacion_trend()
    fig = px.area(df_pop, x="year", y="poblacion",
                  labels={"year": "Año", "poblacion": "Habitantes"},
                  color_discrete_sequence=["#0ea5e9"])
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350,
                      xaxis=dict(dtick=5))
    fig.update_traces(hovertemplate="Año: %{x}<br>Habitantes: %{y:,.0f}<extra></extra>")
    st.plotly_chart(fig, width="stretch")

with col_b:
    st.subheader("📉 Evolución del paro (2008 → 2026)")
    df_paro = paro_trend_total()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_paro["anno"], y=df_paro["paro_hombres"],
                              name="Hombres", line=dict(color="#3b82f6")))
    fig2.add_trace(go.Scatter(x=df_paro["anno"], y=df_paro["paro_mujeres"],
                              name="Mujeres", line=dict(color="#ec4899")))
    fig2.add_trace(go.Scatter(x=df_paro["anno"], y=df_paro["paro_total"],
                              name="Total", line=dict(color="#6b7280", dash="dash")))
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350,
                       xaxis=dict(dtick=2, title="Año"), yaxis_title="Parados medio",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig2, width="stretch")

# ── Fila 2: Paro por distrito ───────────────────────────────────────────
st.subheader("🗺️ Tasa de paro por distrito")
df_dist = paro_por_distrito()
fig3 = px.bar(df_dist, x="tasa_paro", y="distrito", orientation="h",
              text_auto=".1f", color="tasa_paro",
              color_continuous_scale=["#22c55e", "#eab308", "#ef4444"],
              labels={"tasa_paro": "Tasa de paro (%)", "distrito": ""})
fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300,
                   coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig3, width="stretch")

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: El Distrito 01 (casco antiguo) tiene la tasa de paro más alta (25.1%),
mientras el Distrito 02 es el más bajo (16.8%). La ciudad se ha recuperado tras la crisis 2008-2013,
pero el paro femenino sigue siendo sistemáticamente más alto (+34% vs hombres).
""")
