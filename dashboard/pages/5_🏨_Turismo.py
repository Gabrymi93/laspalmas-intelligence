"""
Turismo — Ocupación hotelera, pernoctaciones, gasto por país.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.queries import ocupacion_hotelera, pernottamenti_mensili, spesa_per_paese

st.set_page_config(page_title="Turismo — LPGC", page_icon="🏨", layout="wide")
st.title("🏨 Turismo")

# ── Datos base ──────────────────────────────────────────────────────────
df_hotel = ocupacion_hotelera()
ult_hotel = df_hotel.iloc[-1]
ocupacion = float(ult_hotel["total"])
var_ocup = round(ocupacion - df_hotel.iloc[-2]["total"], 1)

df_pernot = pernottamenti_mensili()
pernot_ult = int(df_pernot[df_pernot["anno"] == df_pernot["anno"].max()]["pernoctaciones"].mean())

# ── KPIs ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ocupación hotelera", f"{ocupacion}%", f"{var_ocup:+.1f} pp vs anterior")
c2.metric("Pernotaciones media", f"{pernot_ult:,.0f}".replace(",", "."))
c3.metric("Hotel 4-5★", f"{float(ult_hotel['altas'])}%")
c4.metric("Hotel 1-3★", f"{float(ult_hotel['bajas'])}%")

st.divider()

# ── Ocupación hotelera trend ────────────────────────────────────────────
st.subheader("📈 Evolución de la ocupación hotelera")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_hotel["anno"], y=df_hotel["total"], name="Total",
                          line=dict(color="#3b82f6", width=3), mode="lines+markers"))
fig1.add_trace(go.Scatter(x=df_hotel["anno"], y=df_hotel["altas"], name="4-5★",
                          line=dict(color="#8b5cf6", dash="dash")))
fig1.add_trace(go.Scatter(x=df_hotel["anno"], y=df_hotel["bajas"], name="1-3★",
                          line=dict(color="#06b6d4", dash="dash")))

# Highlight COVID
fig1.add_vrect(x0=2019.5, x1=2021.5, fillcolor="red", opacity=0.08,
               line_width=0, annotation_text="COVID-19", annotation_position="top")

fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=400,
                   xaxis_title="Año", yaxis_title="Ocupación (%)",
                   yaxis=dict(range=[45, 90]),
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig1, width="stretch")

# ── Pernottamenti mensili ───────────────────────────────────────────────
st.subheader("📊 Pernotaciones mensiles en Gran Canaria")

# Media estacional
df_estacional = df_pernot.groupby("mese")["pernoctaciones"].mean().reset_index()
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
df_estacional["mes_label"] = df_estacional["mese"].apply(lambda x: meses[x-1])

fig2 = px.bar(df_estacional, x="mes_label", y="pernoctaciones",
              color="pernoctaciones",
              color_continuous_scale=["#06b6d4", "#0ea5e9", "#3b82f6"],
              labels={"pernoctaciones": "Pernotaciones", "mes_label": "Mes"})
fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350,
                   coloraxis_showscale=False,
                   xaxis=dict(categoryorder="array", categoryarray=meses))
st.plotly_chart(fig2, width="stretch")

# ── Fila 2: Perfil estacional + Spesa per paese ────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🔄 Perfil estacional")
    media_total = df_estacional["pernoctaciones"].mean()
    df_estacional["indice"] = round(df_estacional["pernoctaciones"] * 100 / media_total, 0)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatterpolar(r=df_estacional["indice"].tolist() + [df_estacional["indice"].iloc[0]],
                                    theta=df_estacional["mes_label"].tolist() + [df_estacional["mes_label"].iloc[0]],
                                    fill="toself", fillcolor="rgba(14,165,233,0.2)",
                                    line=dict(color="#0ea5e9")))
    fig3.add_trace(go.Scatterpolar(r=[100]*12 + [100],
                                    theta=df_estacional["mes_label"].tolist() + [df_estacional["mes_label"].iloc[0]],
                                    line=dict(color="#6b7280", dash="dash"), name="Media"))
    fig3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[50, 130])),
                       margin=dict(l=0, r=0, t=30, b=0), height=400, showlegend=False)
    st.plotly_chart(fig3, width="stretch")

with col_b:
    st.subheader("🌍 Gasto turístico por país de origen")
    df_spesa = spesa_per_paese()
    fig4 = px.treemap(df_spesa, path=["paese"], values="miliardi_eur",
                      color="miliardi_eur",
                      color_continuous_scale=["#06b6d4", "#3b82f6", "#6366f1"],
                      labels={"miliardi_eur": "Miles de millones €", "paese": "País"})
    fig4.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
    st.plotly_chart(fig4, width="stretch")

# ── Insight ─────────────────────────────────────────────────────────────
st.info("""
💡 **Insight clave**: La ocupación hotelera alcanzó un máximo histórico del **82.7%** en 2023,
superando los niveles pre-COVID (73.6% en 2019). El Reino Unido y Alemania concentran el
**53%** del gasto turístico total. El perfil estacional muestra picos en febrero-marzo.
""")
