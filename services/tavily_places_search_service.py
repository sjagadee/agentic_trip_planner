from langchain_tavily import TavilySearch


class TavilyPlacesSearchService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tavily_search_tool = TavilySearch(
            tavily_api_key=self.api_key, topic="general", include_answer="advanced"
        )

    def _extract_answer(self, result):
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def search_attractions(self, location: str):
        """Returns the top attractions in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"Top 10 attractions in and around {location}"}
        )
        return self._extract_answer(result)

    def search_restaurants(self, location: str):
        """Returns the top restaurants in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"Top 10 restaurants and eateries in and around {location}"}
        )
        return self._extract_answer(result)

    def search_cafes(self, location: str):
        """Returns the top cafes in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"Top 10 cafes in and around {location}"}
        )
        return self._extract_answer(result)

    def search_hotels(self, location: str):
        """Returns the top hotels in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"Top 10 hotels in and around {location}"}
        )
        return self._extract_answer(result)

    def search_activities(self, location: str):
        """Returns the top activities in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"What are the different activities to do in and around {location}"}
        )
        return self._extract_answer(result)

    def search_transportation(self, location: str):
        """Returns the top transportation options in a given location"""
        result = self.tavily_search_tool.invoke(
            {"query": f"What are the different transportation options in {location}"}
        )
        return self._extract_answer(result)
