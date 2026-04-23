import requests


class WeatherForecastService:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/forecast.json"

    def get_current_weather(self, location: str) -> dict:
        """Returns the current weather in a given location"""
        try:
            url = self.base_url
            params = {"key": self.api_key, "q": location}
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            raise e

    def get_weather_forecast(self, location: str) -> dict:
        """Returns the weather forecast for a given location"""
        try:
            url = self.base_url
            params = {"key": self.api_key, "q": location, "days": 1}
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            raise e
