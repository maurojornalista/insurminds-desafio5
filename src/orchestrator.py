"""Orquestra WeatherAgent -> RiskAgent -> PolicyAgent -> MessageAgent."""
from __future__ import annotations

from typing import Any

from src.agents import MessageAgent, PolicyAgent, RiskAgent, WeatherAgent
from src.config import POLICYHOLDERS_FILE


class CommunicationOrchestrator:
    """Coordena os quatro agentes e retorna dados prontos para a interface."""

    def __init__(self, weather_agent=None, risk_agent=None, policy_agent=None, message_agent=None):
        self.weather_agent = weather_agent or WeatherAgent()
        self.risk_agent = risk_agent or RiskAgent()
        self.policy_agent = policy_agent or PolicyAgent(POLICYHOLDERS_FILE)
        self.message_agent = message_agent or MessageAgent()

    def run(self, city: str, latitude: float, longitude: float, weather_override: dict[str, Any] | None = None) -> dict[str, Any]:
        weather = weather_override or self.weather_agent.get_weather(latitude, longitude)
        risk = self.risk_agent.assess(weather)
        policyholders = self.policy_agent.find_affected(city, risk)
        communications = [{"policyholder": person, **self.message_agent.generate(person, risk, city)} for person in policyholders]
        return {"weather": weather, "risk": risk, "policyholders": policyholders, "communications": communications}
