from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
from dotenv import load_dotenv
import os
import json
import requests


load_dotenv()
# Middleware (INTEGRATED)
@wrap_model_call
def model_logging(request, handler):
    print("Before model call : ", "-" * 20)
    response = handler(request)
    print("After model call : ", "-" * 20)

    if response.result and response.result[0].content:
        response.result[0].content = response.result[0].content.upper()
    return response


@wrap_model_call
def limit_model_context(request, handler):
    print("* Before model call: ", "-" * 20)
    request.messages = request.messages[-5:]
    response = handler(request)
    print("* After model call: ", "-" * 20)

    if response.result and response.result[0].content:
        response.result[0].content = response.result[0].content.upper()
    return response

#tools
@tool
def calculator(expression: str) -> str:
    """Solve arithmetic expressions"""
    try:
        return str(eval(expression))
    except:
        return "Error"


@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        return json.dumps(requests.get(url).json())
    except:
        return "Error"


@tool
def read_file(filepath: str) -> str:
    """Read text file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Error"


@tool
def knowledge_lookup(query: str) -> str:
    """Simple knowledge base"""
    kb = {
        "langchain": "LangChain is a framework for building LLM-powered applications.",
        "llm": "LLM means Large Language Model."
    }
    return kb.get(query.lower(), "No knowledge found")

#model
llm = init_chat_model(
    model="gemma-3n-e4b-it-text",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

#middle
agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file, knowledge_lookup],
    middleware=[model_logging, limit_model_context],
    system_prompt=(
        "You are a helpful assistant. "
        "Analyze the question. "
        "If a tool is required, call it. "
        "Return a short answer."
    )
)

#chat
conversation = []

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    conversation.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": conversation})

    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)

    conversation = result["messages"]
