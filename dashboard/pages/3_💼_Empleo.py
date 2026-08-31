"""
Empleo — Paro registrado por sexo, edad y barrio.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import (
    paro_mensual_sexo, paro_por_edad_anios, paro_juvenil_barrios,
    barrios_paro_top10,
)

st.set_page_config(page_title="Empleo — LPGC", page_icon="💼", layout="wide")
st.title("💼 Empleo")

# ── Datos base ──────────────────────────────────────────────────────────
df_mensual = paro_mensual_sexo()
ult = df_mensual.iloc[-1]
anterior = df_mensual[df_mensual["anno"] == ult["anno"] - 1].iloc[-1] if len(df_mensual[df_mensual["anno"] == ult["anno"] - 1]) > 0 else ult

paro_total = int(ult["total"])
paro_h = int(ult["hombres"])
paro_m = int(ult["mujeres"])
brecha = round((paro_m - paro_h) * 100 / paro_h, 1)
var_total = round((ult["total"] - anterior["total"]) * 100 / anterior["total"], 1)

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Paro total", f"{paro_total:,}".replace(",", "."), f"{var_total:+.1f}% vs año anterior")
c2.metric("Hombres", f"{paro_h:,}".replace(",", "."))
c3.metric("Mujeres", f"{paro_m:,}".replace(",", "."))
c4.metric("Brecha de género", f"+{brecha}%", "Mujeres sobre hombres")

st.divider()

# ── Evolución del paro por sexo ─────────────────────────────────────────
st.subheader("📈 Evolución del paro por sexo (2008 → 2026)")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_mensual["periodo"], y=df_mensual["mujeres"],
                          name="Mujeres", line=dict(color="#ec4899"), fill="tozeroy",
                          fillcolor="rgba(236,72,153,0.1)"))
fig1.add_trace(go.Scatter(x=df_mensual["periodo"], y=df_mensual["hombres"],
                          name="Hombres", line=dict(color="#3b82f6"), fill="tozeroy",
                          fillcolor="rgba(59,130,246,0.1)"))
fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                   xaxis_title="Período", yaxis_title="Parados",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig1, width="stretch")

# ── Paro por edad (3 años comparativos) ─────────────────────────────────
st.subheader("📊 Perfil del paro por grupo de edad")

df_edad = paro_por_edad_anios()
# Orden de las franjas etarias
orden = ["Y_LT20", "Y20T24", "Y25T29", "Y30T34", "Y35T39", "Y40T44", "Y45T49", "Y50T54", "Y55T59", "Y_GE60"]
labels_cortos = ["<20", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60+"]
map_labels = dict(zip(orden, labels_cortos))

df_edad["edad_corta"] = df_edad["edad_code"].map(map_labels)
df_edad = df_edad[df_edad["edad_corta"].notna()]

fig2 = go.Figure()
for anno, color in [(2008, "#3b82f6"), (2013, "#ef4444"), (2024, "#22c55e")]:
    subset = df_edad[df_edad["anno"] == anno].sort_values("edad_code")
    fig2.add_trace(go.Bar(x=subset["edad_corta"], y=subset["paro_medio"],
                          name=str(anno), marker_color=color))

fig2.update_layout(barmode="group", margin=dict(l=0, r=0, t=10, b=0), height=400,
                   xaxis_title="Grupo de edad", yaxis_title="Parados medio",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig2, width="stretch")

# ── Fila 2: Top barrios + Paro juvenil ──────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏘️ Top 10 barrios con más paro")
    df_top = barrios_paro_top10()
    fig3 = px.bar(df_top, x="tasa_paro", y="barrio", orientation="h",
                  text_auto=".1f", color="tasa_paro",
                  color_continuous_scale=["#eab308", "#ef4444"],
                  labels={"tasa_paro": "Tasa de paro (%)", "barrio": ""})
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                       coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, width="stretch")

with col_b:
    st.subheader("⚠️ Paro juvenil (16-24) vs general")
    df_juv = paro_juvenil_barrios().head(15)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=df_juv["tasa_paro_general"], y=df_juv["barrio"],
                          name="General", orientation="h", marker_color="#3b82f6"))
    fig4.add_trace(go.Bar(x=df_juv["tasa_paro_juvenil"], y=df_juv["barrio"],
                          name="Juvenil (16-24)", orientation="h", marker_color="#ef4444"))
    fig4.update_layout(barmode="group", margin=dict(l=0, r=0, t=10, b=0), height=400,
                       xaxis_title="Tasa de paro (%)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig4, width="stretch")

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: La brecha de género se ha ampliado: las mujeres representan el **57%**
del total de parados (índice de paridad ~134). El paro juvenil duplica sistematicamente al general:
barrios como La Palma y Lomo El Sabinal alcanzan el **50%** entre los 16-24 años.
""")
