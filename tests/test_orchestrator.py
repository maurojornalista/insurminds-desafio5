from src.orchestrator import CommunicationOrchestrator


def test_pipeline_generates_local_communications_for_demo_weather():
    demo_weather = {"available": True, "source": "test", "temperature": 21, "precipitation": 30, "rain": 30, "wind_speed": 20, "weather_code": 65, "error": None}
    result = CommunicationOrchestrator().run("Curitiba", -25.4284, -49.2733, demo_weather)
    assert result["risk"]["has_risk"] is True
    assert len(result["policyholders"]) == 2
    assert len(result["communications"]) == 2
    assert result["communications"][0]["source"] == "Fallback local"
