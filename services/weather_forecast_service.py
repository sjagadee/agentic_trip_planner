from typing import Optional

import requests


class WeatherForecastService:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/forecast.json"

    def get_current_weather(self, location: str) -> Optional[dict]:
        params = {"key": self.api_key, "q": location}
        response = requests.get(self.base_url, params=params, timeout=10)
        return response.json() if response.status_code == 200 else None

    def get_weather_forecast(self, location: str, days: int = 3) -> Optional[dict]:
        params = {"key": self.api_key, "q": location, "days": days}
        response = requests.get(self.base_url, params=params, timeout=10)
        return response.json() if response.status_code == 200 else None
