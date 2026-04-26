import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

from services.google_place_search_service import GooglePlaceSearchService
from services.tavily_places_search_service import TavilyPlacesSearchService


class PlaceSearchTool:

    def __init__(self):
        load_dotenv()
        self.places_api_key = os.getenv("GPLACE_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.google_place_search_service = GooglePlaceSearchService(
            api_key=self.places_api_key
        )
        self.tavily_place_search_service = TavilyPlacesSearchService(
            api_key=self.tavily_api_key
        )
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        google = self.google_place_search_service
        tavily = self.tavily_place_search_service

        @tool
        def search_attractions_google(location: str) -> str:
            """Returns the top attractions in a given location using Google Places"""
            return google.search_attractions(location)

        @tool
        def search_restaurants_google(location: str) -> str:
            """Returns the top restaurants in a given location using Google Places"""
            return google.search_restaurants(location)

        @tool
        def search_cafes_google(location: str) -> str:
            """Returns the top cafes in a given location using Google Places"""
            return google.search_cafes(location)

        @tool
        def search_hotels_google(location: str) -> str:
            """Returns the top hotels in a given location using Google Places"""
            return google.search_hotels(location)

        @tool
        def search_activities_google(location: str) -> str:
            """Returns the top activities in a given location using Google Places"""
            return google.search_activities(location)

        @tool
        def search_transportation_google(location: str) -> str:
            """Returns transportation options in a given location using Google Places"""
            return google.search_transportation(location)

        @tool
        def search_attractions_tavily(location: str) -> str:
            """Returns the top attractions in a given location using Tavily search"""
            return tavily.search_attractions(location)

        @tool
        def search_restaurants_tavily(location: str) -> str:
            """Returns the top restaurants in a given location using Tavily search"""
            return tavily.search_restaurants(location)

        @tool
        def search_cafes_tavily(location: str) -> str:
            """Returns the top cafes in a given location using Tavily search"""
            return tavily.search_cafes(location)

        @tool
        def search_hotels_tavily(location: str) -> str:
            """Returns the top hotels in a given location using Tavily search"""
            return tavily.search_hotels(location)

        @tool
        def search_activities_tavily(location: str) -> str:
            """Returns the top activities in a given location using Tavily search"""
            return tavily.search_activities(location)

        @tool
        def search_transportation_tavily(location: str) -> str:
            """Returns transportation options in a given location using Tavily search"""
            return tavily.search_transportation(location)

        return [
            search_attractions_google,
            search_restaurants_google,
            search_cafes_google,
            search_hotels_google,
            search_activities_google,
            search_transportation_google,
            search_attractions_tavily,
            search_restaurants_tavily,
            search_cafes_tavily,
            search_hotels_tavily,
            search_activities_tavily,
            search_transportation_tavily,
        ]
