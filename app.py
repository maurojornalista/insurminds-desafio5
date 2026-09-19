"""Interface Streamlit do MVP de comunicação climática proativa."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.config import CITIES, DEMO_SCENARIOS
from src.orchestrator import CommunicationOrchestrator

st.set_page_config(page_title="InsurMinds | Comunicação Climática", page_icon="⛅", layout="wide")
st.title("InsurMinds — Comunicação Climática Proativa")
st.write("MVP multiagente que analisa condições meteorológicas, identifica riscos e prepara comunicações preventivas para segurados fictícios.")

city = st.selectbox("Cidade", list(CITIES))
mode = st.radio("Fonte dos dados", ["Clima real", "Cenário de demonstração"], horizontal=True)
scenario = None
if mode == "Cenário de demonstração":
    scenario = st.selectbox("Cenário simulado", list(DEMO_SCENARIOS))
    st.info("Cenário simulado para fins acadêmicos e de demonstração.")

if st.button("Analisar risco", type="primary"):
    location = CITIES[city]
    override = None
    if scenario:
        override = {"available": True, "source": "Cenário de demonstração", **DEMO_SCENARIOS[scenario], "error": None}
    with st.spinner("Executando agentes..."):
        result = CommunicationOrchestrator().run(city, location["latitude"], location["longitude"], override)

    st.subheader("Agente 1 — Coleta Meteorológica")
    weather = result["weather"]
    if weather["available"]:
        columns = st.columns(5)
        fields = [("Temperatura", "temperature", "°C"), ("Precipitação", "precipitation", "mm"), ("Chuva", "rain", "mm"), ("Vento", "wind_speed", "km/h"), ("Weather code", "weather_code", "")]
        for column, (label, key, unit) in zip(columns, fields):
            value = weather.get(key)
            column.metric(label, f"{value if value is not None else 'N/D'} {unit}".strip())
        st.caption(f"Fonte: {weather['source']}")
    else:
        st.warning(weather["error"])

    st.subheader("Agente 2 — Classificação de Risco")
    risk = result["risk"]
    if risk["has_risk"]:
        st.error(f"**{risk['event_type']}** — gravidade {risk['severity']}")
    else:
        st.success("Sem risco climático relevante no momento.")
    st.write(risk["details"])
    st.caption("Apólices potencialmente afetadas: " + (", ".join(risk["affected_policy_types"]) or "nenhuma"))

    st.subheader("Agente 3 — Seleção de Segurados")
    if result["policyholders"]:
        st.dataframe(pd.DataFrame(result["policyholders"]), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum segurado selecionado para esta combinação de cidade e risco.")

    st.subheader("Agente 4 — Geração de Comunicação")
    if result["communications"]:
        for communication in result["communications"]:
            person = communication["policyholder"]
            with st.expander(f"{person['nome']} — {person['tipo_apolice']}", expanded=True):
                st.write(communication["message"])
                st.caption(f"Fonte da mensagem: {communication['source']}")
    else:
        st.info("Não há comunicações a gerar.")
