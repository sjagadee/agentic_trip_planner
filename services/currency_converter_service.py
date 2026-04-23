import requests


class CurrencyConverterService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def convert_currency(
        self, from_currency: str, to_currency: str, amount: float
    ) -> float:
        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_currency}/{to_currency}/{amount}"
            
            response = requests.get(url)
            return (
                response.json()["conversion_result"]
                if response.status_code == 200
                else None
            )
        except Exception as e:
            raise e
