"""Configurações centralizadas e sem segredos do projeto."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
POLICYHOLDERS_FILE = BASE_DIR / "data" / "policyholders.csv"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

CITIES = {
    "São Paulo": {"latitude": -23.5505, "longitude": -46.6333, "estado": "SP"},
    "Rio de Janeiro": {"latitude": -22.9068, "longitude": -43.1729, "estado": "RJ"},
    "Curitiba": {"latitude": -25.4284, "longitude": -49.2733, "estado": "PR"},
    "Porto Alegre": {"latitude": -30.0346, "longitude": -51.2177, "estado": "RS"},
}

DEMO_SCENARIOS = {
    "Chuva intensa": {"temperature": 22.0, "precipitation": 32.0, "rain": 32.0, "wind_speed": 28.0, "weather_code": 65},
    "Vento forte": {"temperature": 20.0, "precipitation": 0.0, "rain": 0.0, "wind_speed": 72.0, "weather_code": 3},
    "Tempestade/granizo": {"temperature": 18.0, "precipitation": 18.0, "rain": 18.0, "wind_speed": 65.0, "weather_code": 99},
}
