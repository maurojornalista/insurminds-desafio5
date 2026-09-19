"""Agente de classificação de risco por regras de negócio explícitas."""
from __future__ import annotations

from typing import Any


class RiskAgent:
    AFFECTED_POLICIES = ["Auto", "Residencial"]

    def assess(self, weather: dict[str, Any]) -> dict[str, Any]:
        if not weather.get("available", True):
            return self._no_risk("Dados meteorológicos indisponíveis para classificação.")
        precipitation = float(weather.get("precipitation") or 0)
        rain = float(weather.get("rain") or 0)
        wind_speed = float(weather.get("wind_speed") or 0)
        weather_code = weather.get("weather_code")
        if weather_code in {95, 96, 99}:
            event = "Tempestade com granizo" if weather_code in {96, 99} else "Tempestade"
            return self._risk(event, "Alta", f"Código meteorológico {weather_code} indica tempestade; vento observado: {wind_speed:.1f} km/h.")
        if precipitation >= 20 or rain >= 20:
            return self._risk("Chuva intensa / risco de alagamento", "Alta", f"Precipitação atual de {precipitation:.1f} mm e chuva de {rain:.1f} mm.")
        if wind_speed >= 60:
            return self._risk("Vento forte / risco de vendaval", "Média", f"Vento atual de {wind_speed:.1f} km/h, acima do limiar de 60 km/h.")
        return self._no_risk("Nenhum limiar de risco climático foi atingido nas condições atuais.")

    def _risk(self, event_type: str, severity: str, details: str) -> dict[str, Any]:
        return {"has_risk": True, "event_type": event_type, "severity": severity, "details": details, "affected_policy_types": self.AFFECTED_POLICIES}

    @staticmethod
    def _no_risk(details: str) -> dict[str, Any]:
        return {"has_risk": False, "event_type": "Sem risco relevante", "severity": "Baixa", "details": details, "affected_policy_types": []}
