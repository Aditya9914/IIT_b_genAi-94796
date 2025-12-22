# Q2:
# Create a Streamlit application that takes a city name as input from the user.
# Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize LLM (Groq)
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("🌍 City Weather Explainer")
st.subheader("Enter a city name to get current weather explained simply")

city_name = st.text_input("City name")

# Weather API key
weather_api_key = "10575925b2f79fb195fad9ad6ca12654"

if st.button("Get Weather") and city_name:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        weather = response.json()

        condition = weather["weather"][0]["main"]
        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]

        st.write(f"🌡 **Temperature:** {temp} °C")
        st.write(f"💧 **Humidity:** {humidity} %")
        st.write(f"🌬 **Wind Speed:** {wind} m/s")

        # LLM prompt
        prompt = f"""
        The current weather in {city_name} is {condition}.
        Temperature is {temp}°C, humidity is {humidity}%,
        and wind speed is {wind} m/s.
        Explain this weather in very simple English.
        """

        # Call LLM
        response = llm.invoke(prompt)

        st.subheader("🧠 AI Explanation")
        st.write(response.content)

    else:
        st.error("❌ City not found")
