import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

from services.place_search_service import PlaceSearchService


class PlaceSearchTool:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.place_search_service = PlaceSearchService(api_key=self.api_key)
        self.place_search_tool_list = self._setup_tools()