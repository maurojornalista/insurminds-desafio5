from src.agents.message_agent import MessageAgent


def test_fallback_is_specific_to_policy_and_event():
    agent = MessageAgent()
    risk = {"event_type": "Chuva intensa / risco de alagamento", "severity": "Alta"}
    auto = agent._fallback({"nome": "Ana", "tipo_apolice": "Auto"}, risk, "São Paulo")
    residential = agent._fallback({"nome": "Bruno", "tipo_apolice": "Residencial"}, risk, "São Paulo")

    assert "Ana" in auto and "São Paulo" in auto
    assert "vias com histórico de alagamento" in auto
    assert "Bruno" in residential and "ralos e calhas" in residential
    assert auto != residential


def test_fallback_has_vendaval_and_storm_guidance():
    agent = MessageAgent()
    auto = agent._fallback({"nome": "Carla", "tipo_apolice": "Auto"}, {"event_type": "Vento forte / risco de vendaval"}, "Curitiba")
    residential = agent._fallback({"nome": "Diego", "tipo_apolice": "Residencial"}, {"event_type": "Tempestade com granizo"}, "Curitiba")

    assert "árvores" in auto
    assert "janelas" in residential
    assert "alertas oficiais" in auto and "alertas oficiais" in residential
