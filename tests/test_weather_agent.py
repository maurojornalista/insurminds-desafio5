from src.agents.weather_agent import WeatherAgent


def test_parses_next_twelve_hourly_observations():
    hourly = {
        "time": ["2026-09-19T19:00", "2026-09-19T20:00", "2026-09-19T21:00", "2026-09-19T22:00"],
        "precipitation": [0.0, 0.2, 1.5, 0.0],
        "rain": [0.0, 0.2, 1.5, 0.0],
        "wind_speed_10m": [10, 12, 15, 13],
        "weather_code": [3, 51, 61, 3],
    }

    forecast = WeatherAgent._next_12_hours("2026-09-19T20:00", hourly)

    assert len(forecast) == 3
    assert forecast[0]["time"] == "2026-09-19T20:00"
    assert forecast[1]["precipitation"] == 1.5
    assert forecast[2]["wind_speed"] == 13
