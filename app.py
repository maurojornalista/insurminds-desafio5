"""Interface Streamlit do MVP de comunicação climática proativa."""
from __future__ import annotations

from datetime import datetime
from html import escape

import pandas as pd
import streamlit as st

from src.config import CITIES, DEMO_SCENARIOS
from src.orchestrator import CommunicationOrchestrator


def weather_icon(weather_code: int | None, event_type: str = "") -> str:
    """Traduz códigos WMO e eventos de risco em um ícone simples."""
    if "tempestade" in event_type.casefold() or weather_code in {95, 96, 99}:
        return "⛈️"
    if weather_code is not None and 51 <= weather_code <= 82:
        return "🌧️"
    if weather_code == 0:
        return "☀️"
    if weather_code is not None and 1 <= weather_code <= 3:
        return "☁️"
    return "⛅"


def risk_presentation(risk: dict) -> tuple[str, str, str]:
    if not risk["has_risk"]:
        return "risk-green", "🟢", "Sem risco relevante"
    if risk["severity"] == "Alta":
        return "risk-red", "🔴", "Risco alto"
    return "risk-yellow", "🟡", "Risco moderado"


st.set_page_config(page_title="InsurMinds | Comunicação Climática", page_icon="⛅", layout="wide")
st.markdown(
    """
    <style>
    .hero {padding: 2rem 2.2rem; border-radius: 18px; color: white;
           background: linear-gradient(120deg, #0f4c81, #117a8b 55%, #25a18e); margin-bottom: 1.5rem;}
    .hero h1 {margin: 0; font-size: 2.1rem;} .hero p {margin: .55rem 0 0; font-size: 1.05rem; opacity: .95;}
    .risk-card {padding: 1.15rem 1.35rem; border-radius: 14px; margin: .4rem 0 1rem;}
    .risk-green {background: #e8f7ed; border-left: 7px solid #2e9d57; color: #155d2e;}
    .risk-yellow {background: #fff7db; border-left: 7px solid #e5a100; color: #775500;}
    .risk-red {background: #ffebee; border-left: 7px solid #d83a4a; color: #8a1826;}
    .message-card {padding: 1rem 1.15rem; border: 1px solid #dce8ef; border-radius: 12px; margin-bottom: .8rem; background: #fbfdff;}
    .source-pill {display: inline-block; border-radius: 999px; padding: .25rem .7rem; background: #e6f4f1; color: #126b61; font-weight: 600;}
    </style>
    <section class="hero"><h1>⛅ InsurMinds — Comunicação Climática Proativa</h1>
    <p>Uma experiência multiagente para identificar riscos meteorológicos e preparar comunicações preventivas para segurados.</p></section>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2, 1])
with left:
    city = st.selectbox("Cidade monitorada", list(CITIES))
with right:
    mode = st.radio("Fonte dos dados", ["Clima real", "Cenário de demonstração"], horizontal=False)

scenario = None
if mode == "Cenário de demonstração":
    scenario = st.selectbox("Cenário simulado", list(DEMO_SCENARIOS))
    st.info("Cenário simulado para fins acadêmicos e de demonstração.")

if st.button("Analisar risco", type="primary", use_container_width=True):
    location = CITIES[city]
    override = None
    if scenario:
        override = {"available": True, "source": "Cenário de demonstração", **DEMO_SCENARIOS[scenario], "error": None}

    queried_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with st.spinner("Executando agentes..."):
        result = CommunicationOrchestrator().run(city, location["latitude"], location["longitude"], override)

    weather = result["weather"]
    risk = result["risk"]
    icon = weather_icon(weather.get("weather_code"), risk["event_type"])
    source_label = "Open-Meteo (clima real)" if weather["source"] == "Open-Meteo" else "Cenário de demonstração"
    st.markdown(f"<span class='source-pill'>{icon} Fonte: {source_label}</span>", unsafe_allow_html=True)

    st.subheader("Agente 1 — Coleta Meteorológica")
    if weather["available"]:
        columns = st.columns(5)
        fields = [
            ("Temperatura", "temperature", "°C", "🌡️"),
            ("Precipitação", "precipitation", "mm", "💧"),
            ("Chuva", "rain", "mm", "🌧️"),
            ("Vento", "wind_speed", "km/h", "💨"),
            ("Condição", "weather_code", "", icon),
        ]
        for column, (label, key, unit, metric_icon) in zip(columns, fields):
            value = weather.get(key)
            column.metric(f"{metric_icon} {label}", f"{value if value is not None else 'N/D'} {unit}".strip())

        chart_data = pd.DataFrame(
            {"Indicador": ["Precipitação (mm)", "Chuva (mm)", "Vento (km/h)"],
             "Valor": [weather.get("precipitation") or 0, weather.get("rain") or 0, weather.get("wind_speed") or 0]}
        ).set_index("Indicador")
        st.caption("Indicadores atuais — comparação visual de precipitação, chuva e vento.")
        st.bar_chart(chart_data, color="#117a8b")
    else:
        st.warning(weather["error"])

    st.subheader("Agente 2 — Classificação de Risco")
    card_class, risk_icon, risk_label = risk_presentation(risk)
    st.markdown(
        f"<div class='risk-card {card_class}'><strong>{risk_icon} {risk_label}</strong><br>"
        f"<span style='font-size:1.15rem'>{icon} {escape(risk['event_type'])}</span> · Gravidade: <strong>{escape(risk['severity'])}</strong><br>"
        f"{escape(risk['details'])}</div>",
        unsafe_allow_html=True,
    )
    st.caption("Apólices potencialmente afetadas: " + (", ".join(risk["affected_policy_types"]) or "nenhuma"))

    st.subheader("Agente 3 — Seleção de Segurados")
    policyholders = result["policyholders"]
    st.metric("Segurados selecionados", len(policyholders))
    if policyholders:
        selected_columns = ["nome", "cidade", "tipo_apolice", "veiculo_ou_imovel", "contato"]
        table = pd.DataFrame(policyholders)[selected_columns].rename(columns={"nome": "Nome", "cidade": "Cidade", "tipo_apolice": "Apólice", "veiculo_ou_imovel": "Bem segurado", "contato": "Contato"})
        st.dataframe(table, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum segurado selecionado para esta combinação de cidade e risco.")

    st.subheader("Agente 4 — Geração de Comunicação")
    if result["communications"]:
        for communication in result["communications"]:
            person = communication["policyholder"]
            st.markdown(
                f"<div class='message-card'><strong>✉️ {escape(str(person['nome']))}</strong> "
                f"<span style='color:#557'>· Seguro {escape(str(person['tipo_apolice']))}</span><br><br>"
                f"{escape(communication['message'])}<br><br><small>Fonte da mensagem: {escape(communication['source'])}</small></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Não há comunicações a gerar.")

    with st.expander("Dados brutos da API", expanded=False):
        st.write(f"**Fonte dos dados:** {source_label}")
        st.write(f"**Horário da consulta:** {queried_at}")
        st.write(f"**Coordenadas:** latitude {location['latitude']}, longitude {location['longitude']}")
        st.write("**Resposta resumida:**")
        st.json({key: value for key, value in weather.items() if key != "error"})
