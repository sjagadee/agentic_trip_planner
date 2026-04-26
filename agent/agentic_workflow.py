from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools.weather_forecast_tool import WeatherForecastTool
from tools.arithmetic_calculator_tool import ArithmeticCalculatorTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_converter_tool import CurrencyConverterTool

from utils.model_loader import ModelLoader

from prompt_library.prompt import SYSTEM_PROMPT


class GraphBuilder:

    def __init__(self, model_provider: str = "openai"):
        self.system_prompt = SYSTEM_PROMPT
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []

        self.weather_tool = WeatherForecastTool()
        self.arithmetic_calculator_tool = ArithmeticCalculatorTool()
        self.place_search_tool = PlaceSearchTool()
        self.expense_calculator_tool = CalculatorTool()
        self.currency_converter_tool = CurrencyConverterTool()

        self.tools.extend(self.weather_tool.weather_tool_list)
        self.tools.extend(self.place_search_tool.place_search_tool_list)
        self.tools.extend(self.expense_calculator_tool.expense_tool_list)
        self.tools.extend(self.currency_converter_tool.currency_tool_list)
        self.tools.extend(self.arithmetic_calculator_tool.calculator_tool_list)

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        self.graph = None

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent", tools_condition
        )  # handles END condition if no tools match
        graph_builder.add_edge("tools", "agent")

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
