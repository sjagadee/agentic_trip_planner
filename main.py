import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent.agentic_workflow import GraphBuilder

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)

        graph = GraphBuilder(model_provider="groq")
        reactive_app = graph()

        png_graph = reactive_app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph in PNG format saved as graph.png in {os.getcwd()}")

        messages = {"messages": [HumanMessage(content=query.query)]}
        output = reactive_app.invoke(messages)

        # capture last message from output
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
