"""
Economía — Renta, empresas, autónomos, coworking.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    kpi_empresas, renta_por_distrito, empresas_evolucion,
    autonomos_trend, demanda_coworking, autonomos_sectores,
)

st.set_page_config(page_title="Economía — LPGC", page_icon="💰", layout="wide")
st.title("💰 Economía")

# ── Datos base ──────────────────────────────────────────────────────────
df_auto = autonomos_trend()
df_cow = demanda_coworking()
autonomos_act = int(df_auto[df_auto["year"] == df_auto["year"].max()]["autonomos"].iloc[0])
autonomos_prev = int(df_auto[df_auto["year"] == df_auto["year"].max() - 1]["autonomos"].iloc[0]) if len(df_auto[df_auto["year"] == df_auto["year"].max() - 1]) > 0 else autonomos_act
var_aut = round((autonomos_act - autonomos_prev) * 100 / autonomos_prev, 1)
demanda_cow = int(df_cow.iloc[-1]["demanda"])
por_mil = float(df_cow.iloc[-1]["por_mil_hab"])

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Empresas", f"{kpi_empresas():,}".replace(",", "."))
c2.metric("Autónomos", f"{autonomos_act:,}".replace(",", "."), f"{var_aut:+.1f}% vs anterior")
c3.metric("Demanda coworking", f"{demanda_cow:,}".replace(",", "."))
c4.metric("Por cada 1.000 hab.", f"{por_mil}")

st.divider()

# ── Renta por distrito (stacked bar) ────────────────────────────────────
st.subheader("📊 Composición de la renta por distrito (2023)")

df_renta = renta_por_distrito()
# Formato largo para plotly
df_renta_long = df_renta.melt(id_vars="distrito", var_name="fuente", value_name="pct")
map_fuentes = {"sueldos": "Sueldos y salarios", "pensiones": "Pensiones",
               "desempleo": "Prest. desempleo", "otros": "Otros ingresos"}
df_renta_long["fuente"] = df_renta_long["fuente"].map(map_fuentes)

fig1 = px.bar(df_renta_long, x="distrito", y="pct", color="fuente",
              color_discrete_map={"Sueldos y salarios": "#3b82f6", "Pensiones": "#8b5cf6",
                                  "Prest. desempleo": "#ef4444", "Otros ingresos": "#6b7280"},
              labels={"pct": "% de la renta", "distrito": "", "fuente": "Fuente"})
fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400, barmode="stack",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig1, width="stretch")

# ── Fila 2: Empresas evolución + Autónomos ──────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏢 Evolución de empresas por tamaño")
    df_emp = empresas_evolucion()
    # Orden de tamaños
    orden = ["1-9 asalariados", "10-49 asalariados", "50-249 asalariados", "250+ asalariados"]
    colores = ["#0ea5e9", "#3b82f6", "#6366f1", "#8b5cf6"]
    fig2 = go.Figure()
    for label, color in zip(orden, colores):
        subset = df_emp[df_emp["estrato_label"] == label]
        if len(subset) > 0:
            fig2.add_trace(go.Scatter(x=subset["year"], y=subset["media"], name=label,
                                      mode="lines", stackgroup="one", line=dict(color=color)))
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                       xaxis_title="Año", yaxis_title="Empresas",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig2, width="stretch")

with col_b:
    st.subheader("👩‍💼 Evolución de autónomos")
    fig3 = px.line(df_auto, x="year", y="autonomos", markers=True,
                   color_discrete_sequence=["#f59e0b"])
    fig3.update_traces(hovertemplate="Año: %{x}<br>Autónomos: %{y:,.0f}<extra></extra>")
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                       xaxis_title="Año", yaxis_title="Autónomos")
    st.plotly_chart(fig3, width="stretch")

# ── Demanda de coworking ────────────────────────────────────────────────
st.subheader("💻 Demanda potencial de coworking")

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=df_cow["year"], y=df_cow["por_mil_hab"], name="Demanda por 1.000 hab.",
                          mode="lines+markers", line=dict(color="#6366f1"), yaxis="y1"))
fig4.add_trace(go.Bar(x=df_cow["year"], y=df_cow["demanda"], name="Demanda total",
                      marker_color="rgba(99,102,241,0.3)", yaxis="y2"))
fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350,
                   xaxis_title="Año",
                   yaxis=dict(title="Por 1.000 hab.", side="left"),
                   yaxis2=dict(title="Demanda total", side="right", overlaying="y"),
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig4, width="stretch")

# ── Top 15 sectores autónomos ───────────────────────────────────────────
st.subheader("🏭 Principales sectores de autónomos")

asect = autonomos_sectores()
# Acortar nombres largos
asect["sector_corto"] = asect["sector"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

fig5 = px.bar(asect, x="media", y="sector_corto", orientation="h",
              text_auto=".0f", color="media",
              color_continuous_scale=["#0ea5e9", "#3b82f6"],
              labels={"media": "Autónomos (media)", "sector_corto": ""})
fig5.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=500,
                   coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig5, width="stretch")

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: Las microempresas (1-9 asalariados) dominan con el **80%** del total.
La demanda potencial de coworking ha crecido un **86.8 por cada 1.000 habitantes** en 2024.
El sector comercio lidera los autónomos (5.093), seguido de actividades profesionales (2.912).
""")
