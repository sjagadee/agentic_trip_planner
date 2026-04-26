from langchain_google_community import GooglePlacesAPIWrapper, GooglePlacesTool


class GooglePlaceSearchService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=self.api_key)
        self.places_search_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)

    def search_attractions(self, location: str):
        """Returns the top attractions in a given location"""
        return self.places_search_tool.invoke(
            f"Top 10 attractions in and around {location}"
        )

    def search_restaurants(self, location: str):
        """Returns the top restaurants in a given location"""
        return self.places_search_tool.invoke(
            f"Top 10 restaurants in and around {location}"
        )

    def search_hotels(self, location: str):
        """Returns the top hotels in a given location"""
        return self.places_search_tool.invoke(f"Top 10 hotels in and around {location}")

    def search_cafes(self, location: str):
        """Returns the top cafes in a given location"""
        return self.places_search_tool.invoke(f"Top 10 cafes in and around {location}")

    def search_activities(self, location: str):
        """Returns the top activities in a given location"""
        return self.places_search_tool.invoke(
            f"What are the different activities to do in and around {location}"
        )

    def search_transportation(self, location: str):
        """Returns the top transportation options in a given location"""
        return self.places_search_tool.invoke(
            f"What are the different transportation options in {location}"
        )
