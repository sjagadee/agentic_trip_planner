import os
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv
from langchain.tools import BaseTool, tool
from dotenv import load_dotenv

from utils.weather_info import WeatherForecastService


class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.weather_service = WeatherForecastService(api_key=self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast service"""

        @tool
        def get_current_weather(location: str) -> str:
            """Returns the current weather in a given location"""
            weather_data = self.weather_service.get_current_weather(location)
            if weather_data:
                temp = weather_data.get("current", {}).get("temp_c", "N/A")
                descriptions = (
                    weather_data.get("current", {})
                    .get("condition", {})
                    .get("text", "N/A")
                )
                return f"The current weather in {location} is {descriptions} with a temperature of {temp} degrees celsius."
            return f"Unable to get weather information for {location}"

        @tool
        def get_weather_forecast(location: str) -> str:
            """Returns the weather forecast for a given location"""
            weather_data = self.weather_service.get_weather_forecast(location)
            if weather_data:
                forecast = weather_data.get("forecast", {})
                forecast_data = forecast.get("forecastday", [])
                desc = (
                    forecast_data[0]
                    .get("day", {})
                    .get("condition", {})
                    .get("text", "N/A")
                )
                temp = forecast_data[0].get("day", {}).get("avgtemp_c", "N/A")
                precep = forecast_data[0].get("day", {}).get("totalprecip_in", "N/A")
                wind = forecast_data[0].get("day", {}).get("maxwind_kph", "N/A")
                return f"The weather forecast for {location} is {desc} with an average temperature of {temp} degrees celsius, a precipitation of {precep} inches, and a wind speed of {wind} kph."
            return f"Unable to get weather forecast information for {location}"

        return [get_current_weather, get_weather_forecast]
