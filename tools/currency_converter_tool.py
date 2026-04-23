import os
from typing import Any, Dict, Optional, List
from dotenv import load_dotenv
from langchain.tools import BaseTool, tool
from dotenv import load_dotenv

from utils.currency_converter import CurrencyConverterService


class CurrencyConverterTool:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverterService(api_key=self.api_key)
        self.currency_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def convert_currency(
            from_currency: str, to_currency: str, amount: float
        ) -> str:
            """Converts a given amount of currency from one currency to another"""
            converted_amount = self.currency_service.convert_currency(
                from_currency, to_currency, amount
            )
            return (
                f"{amount} {from_currency} is equal to {converted_amount} {to_currency}"
            )

        return [convert_currency]
