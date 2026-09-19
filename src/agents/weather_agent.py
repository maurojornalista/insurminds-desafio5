"""Agente responsável pela coleta de condições meteorológicas atuais."""
from __future__ import annotations

from typing import Any

import requests


class WeatherAgent:
    """Consulta a API pública Open-Meteo sem exigir chave de API."""

    URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m,precipitation,rain,wind_speed_10m,weather_code", "wind_speed_unit": "kmh", "timezone": "auto"}
        try:
            response = requests.get(self.URL, params=params, timeout=10)
            response.raise_for_status()
            current = response.json().get("current", {})
            return {"available": True, "source": "Open-Meteo", "temperature": current.get("temperature_2m"), "precipitation": current.get("precipitation"), "rain": current.get("rain"), "wind_speed": current.get("wind_speed_10m"), "weather_code": current.get("weather_code"), "error": None}
        except (requests.RequestException, ValueError, KeyError) as exc:
            return {"available": False, "source": "Open-Meteo", "temperature": None, "precipitation": None, "rain": None, "wind_speed": None, "weather_code": None, "error": f"Não foi possível consultar o clima: {exc}"}
