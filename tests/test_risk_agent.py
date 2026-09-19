from src.agents.risk_agent import RiskAgent


def test_classifies_heavy_rain_as_high_risk():
    result = RiskAgent().assess({"available": True, "precipitation": 25, "rain": 25, "wind_speed": 10, "weather_code": 61})
    assert result["has_risk"] is True
    assert result["severity"] == "Alta"
    assert "Chuva intensa" in result["event_type"]
    assert result["affected_policy_types"] == ["Auto", "Residencial"]


def test_returns_no_risk_for_calm_weather():
    result = RiskAgent().assess({"available": True, "precipitation": 0, "rain": 0, "wind_speed": 15, "weather_code": 1})
    assert result["has_risk"] is False
    assert result["affected_policy_types"] == []
