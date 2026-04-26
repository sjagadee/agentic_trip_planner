# Voyage — AI Travel Concierge

*Tell it where you want to go. Get a full trip plan back — flights, hotels, food, weather, budget, and all.*

Voyage is an AI-powered travel planning agent built with LangGraph and LangChain. You describe a trip in plain English, and the agent does the heavy lifting: it searches real places, checks the weather, converts currencies, and compiles everything into a day-by-day itinerary — including an off-beat route most tourists never find.

---

## What it does

You type something like:

> *"Plan a 7-day trip to Kyoto in autumn for 2 people on a medium budget"*

And Voyage gives you back:

- Two complete itineraries — one classic tourist route, one off-beat local path
- Day-by-day plans with specific places and timings
- Hotel recommendations with approximate nightly costs
- Top restaurants, cafes, and local eats with price ranges
- Activities and experiences with details
- Transport options available in the city
- Full cost breakdown and a daily budget estimate
- Live weather forecast for the destination

Everything in one clean, formatted response.

---

## How it works

Voyage is a **ReAct agent** — it reasons step by step and calls real tools to gather data before writing your plan.

```
User Query
    │
    ▼
FastAPI Backend (port 8000)
    │
    ▼
LangGraph Agent  ──── Decides which tools to call
    │
    ├── Weather Tool        → WeatherAPI (current + forecast)
    ├── Place Search Tool   → Google Places + Tavily (attractions, hotels, restaurants, cafes, activities, transport)
    ├── Currency Converter  → Exchange Rate API
    └── Expense Calculator  → calculates totals and daily budgets
    │
    ▼
LLM (Groq Llama 3.3 70B  or  OpenAI GPT-4o-mini)
    │
    ▼
Streamlit UI — renders your itinerary
```

The agent loops between reasoning and tool calls until it has enough information, then writes the final plan. LangGraph manages the state across the whole conversation.

---

## Tech stack

| Layer | Technology |
|---|---|
| Agent framework | LangGraph + LangChain |
| LLM options | Groq (Llama 3.3 70B) · OpenAI (GPT-4o-mini) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Package manager | uv |
| Python | 3.11+ |

---

## Project structure

```
TravelPlanner/
├── agent/
│   └── agentic_workflow.py     # LangGraph graph — wires agent + tools together
├── tools/                      # LangChain tool wrappers (what the agent can call)
│   ├── weather_forecast_tool.py
│   ├── place_search_tool.py
│   ├── currency_converter_tool.py
│   ├── expense_calculator_tool.py
│   └── arithmetic_calculator_tool.py
├── services/                   # Raw API clients called by each tool
│   ├── weather_forecast_service.py
│   ├── google_place_search_service.py
│   ├── tavily_places_search_service.py
│   ├── currency_converter_service.py
│   └── expense_calculator_service.py
├── prompt_library/
│   └── prompt.py               # System prompt that shapes how the agent responds
├── utils/
│   ├── model_loader.py         # Loads the right LLM based on config
│   └── config_loader.py        # Reads config/config.yaml
├── config/
│   └── config.yaml             # Model names and providers
├── main.py                     # FastAPI app — the /query endpoint
├── streamlit_app.py            # The browser UI
└── pyproject.toml
```

---

## Getting started

### 1. Clone and install

```bash
git clone <your-repo-url>
cd TravelPlanner

# Install uv if you don't have it
pip install uv

# Install dependencies
uv sync
```

### 2. Set up your API keys

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Open `.env` and add:

```env
# LLM — pick at least one
GROQ_API_KEY=""          # free tier available at console.groq.com
OPENAI_API_KEY=""        # platform.openai.com

# Place search — pick at least one
GPLACES_API_KEY=""       # Google Places API (console.cloud.google.com)
TAVILY_API_KEY=""        # tavily.com — free tier available

# Weather
WEATHER_API_KEY=""       # weatherapi.com — free tier available

# Currency conversion
EXCHANGE_RATE_API_KEY="" # exchangerate-api.com — free tier available

# Optional: LangSmith tracing (useful for debugging)
LANGCHAIN_TRACING_V2=""
LANGCHAIN_API_KEY=""
LANGCHAIN_PROJECT=""
LANGCHAIN_ENDPOINT=""
```

> You need **at minimum**: one LLM key, one place search key, a weather key, and a currency key for the agent to function fully.

### 3. Run the backend

```bash
uv run python main.py
```

The FastAPI server starts on `http://localhost:8000`. You can also explore the API at `http://localhost:8000/docs`.

### 4. Run the frontend

In a separate terminal:

```bash
uv run streamlit run streamlit_app.py
```

Open the link Streamlit prints (usually `http://localhost:8501`). Type your trip query and hit **Plan My Journey**.

---

## Switching LLM providers

The backend defaults to **Groq** (fast, free). To switch to OpenAI, update this line in `main.py`:

```python
# Groq (default)
graph = GraphBuilder(model_provider="groq")

# OpenAI
graph = GraphBuilder(model_provider="openai")
```

Model names are configured in [config/config.yaml](config/config.yaml):

```yaml
llm:
  openai:
    model_name: "gpt-4o-mini"
  groq:
    model_name: "llama-3.3-70b-versatile"
```

---

## API usage

You can also call the backend directly without the UI:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Plan a 5-day trip to Lisbon in spring for one person"}'
```

Response:

```json
{
  "answer": "## Lisbon 5-Day Itinerary\n\n..."
}
```

---

## Tools the agent can use

| Tool | What it does |
|---|---|
| `get_current_weather` | Live weather for any city |
| `get_weather_forecast` | Tomorrow's forecast (temp, rain, wind) |
| `search_attractions_google/tavily` | Top sights and landmarks |
| `search_restaurants_google/tavily` | Best places to eat |
| `search_cafes_google/tavily` | Cafes and coffee spots |
| `search_hotels_google/tavily` | Hotels and accommodation |
| `search_activities_google/tavily` | Things to do — tours, experiences |
| `search_transportation_google/tavily` | Getting around the city |
| `convert_currency` | Live exchange rates between any currencies |
| `calculate_total` | Adds up a list of expenses |
| `calculate_daily_budget` | Breaks total cost into a per-day figure |

Each tool has a Google Places and a Tavily version — the agent picks whichever gives better results.

---

## Example queries

- `"7 days in Tokyo in April, budget $3000"`
- `"Weekend trip to Amsterdam, solo traveler, mid-range budget"`
- `"Plan a honeymoon trip to Maldives for 5 days"`
- `"3-day food trip to Bangkok — I want to eat everything"`
- `"Family trip to Costa Rica for 10 days with two kids"`

---

## Development

Run tests:

```bash
uv run pytest
```

Lint:

```bash
uv run ruff check .
```

The graph visualization is saved as `graph.png` in the project root each time the backend handles a request — useful for understanding how the agent flow is structured.

---

## Requirements

- Python 3.11+
- At least one LLM API key (Groq recommended — it's free and fast)
- WeatherAPI key (free tier is enough)
- Google Places or Tavily key for place search
- Exchange Rate API key for currency conversion
