import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

from services.expense_calculator_service import ExpenseCalculatorService


class CurrencyConverterTool:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.expense_calculator_service = ExpenseCalculatorService(api_key=self.api_key)
        self.expense_tool_list = self._setup_tools()

    