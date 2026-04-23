from typing import List
from langchain.tools import tool

from services.calculator_service import CalculatorService


class ArithmaticCalculatorTool:
    def __init__(self):
        self.calculator_service = CalculatorService()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:

        @tool
        def add_tool(a: float, b: float) -> float:
            """
            Returns the sum of two numbers

            Args:
                a (float): The first number
                b (float): The second number

            Returns:
                float: The sum of the two numbers
            """
            return self.calculator_service.add(a, b)

        @tool
        def subtract_tool(a: float, b: float) -> float:
            """
            Returns the difference between two numbers

            Args:
                a (float): The first number
                b (float): The second number

            Returns:
                float: The difference between the two numbers
            """
            return self.calculator_service.subtract(a, b)

        @tool
        def multiply_tool(a: float, b: float) -> float:
            """
            Returns the product of two numbers

            Args:
                a (float): The first number
                b (float): The second number

            Returns:
                float: The product of the two numbers
            """
            return self.calculator_service.multiply(a, b)

        @tool
        def divide_tool(a: float, b: float) -> float:
            """
            Returns the quotient of two numbers

            Args:
                a (float): The first number
                b (float): The second number

            Returns:
                float: The quotient of the two numbers
            """
            return self.calculator_service.divide(a, b)

        return [add_tool, subtract_tool, multiply_tool, divide_tool]
