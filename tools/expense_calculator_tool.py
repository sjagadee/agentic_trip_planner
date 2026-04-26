from typing import List
from langchain.tools import tool

from services.expense_calculator_service import ExpenseCalculatorService


class CalculatorTool:

    def __init__(self):
        self.expense_calculator_service = ExpenseCalculatorService()
        self.expense_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:

        @tool
        def calculate_total(expenses: List[float]) -> float:
            """
            Calculate the total amount of a list of expenses.

            Args:
                expenses: A list of expense amounts.

            Returns:
                float: The total sum of all expenses.
            """
            return self.expense_calculator_service.calculate_total(*expenses)

        @tool
        def calculate_daily_budget(total: float, days: int) -> str:
            """
            Calculate the daily budget based on total amount and number of days.

            Args:
                total: The total amount of expenses.
                days: The number of days (must be greater than zero).

            Returns:
                str: The daily budget or an error message.
            """
            try:
                return str(self.expense_calculator_service.calculate_daily_budget(total, days))
            except ValueError as e:
                return str(e)

        return [calculate_total, calculate_daily_budget]
