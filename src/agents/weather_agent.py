"""Agente responsável pela coleta de condições meteorológicas atuais."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import requests


class WeatherAgent:
    """Consulta a API pública Open-Meteo sem exigir chave de API."""

    URL = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation,rain,wind_speed_10m,weather_code",
            "hourly": "precipitation,rain,wind_speed_10m,weather_code",
            "forecast_days": 2,
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        }
        try:
            response = requests.get(self.URL, params=params, timeout=10)
            response.raise_for_status()
            payload = response.json()
            current = payload.get("current", {})
            return {
                "available": True,
                "source": "Open-Meteo",
                "temperature": current.get("temperature_2m"),
                "precipitation": current.get("precipitation"),
                "rain": current.get("rain"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
                "hourly_forecast": self._next_12_hours(current.get("time"), payload.get("hourly", {})),
                "error": None,
            }
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            return {
                "available": False,
                "source": "Open-Meteo",
                "temperature": None,
                "precipitation": None,
                "rain": None,
                "wind_speed": None,
                "weather_code": None,
                "hourly_forecast": [],
                "error": f"Não foi possível consultar o clima: {exc}",
            }

    @staticmethod
    def _next_12_hours(current_time: str | None, hourly: dict[str, list[Any]]) -> list[dict[str, Any]]:
        """Normaliza as primeiras 12 horas futuras do retorno local da Open-Meteo."""
        times = hourly.get("time", [])
        if not times:
            return []
        now = datetime.fromisoformat(current_time) if current_time else None
        forecast = []
        for index, time_value in enumerate(times):
            hour = datetime.fromisoformat(time_value)
            if now and hour < now:
                continue
            forecast.append(
                {
                    "time": time_value,
                    "precipitation": (hourly.get("precipitation", [None] * len(times))[index]),
                    "rain": (hourly.get("rain", [None] * len(times))[index]),
                    "wind_speed": (hourly.get("wind_speed_10m", [None] * len(times))[index]),
                    "weather_code": (hourly.get("weather_code", [None] * len(times))[index]),
                }
            )
            if len(forecast) == 12:
                break
        return forecast
