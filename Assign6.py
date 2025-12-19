import os
import requests
import json
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for model selection
st.sidebar.title("Model Selection")
model_choice = st.sidebar.radio("Choose a model:", ("Groq", "LM Studio"))

# Input for user question
user_question = st.text_input("Enter your question:")

# Function to get response from Groq
def get_groq_response(question):
    api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    return response.json()["choices"][0]["message"]["content"]

# Function to get response from LM Studio
def get_lm_studio_response(question):
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma-3n-e4b-it-text",
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Display chat history
for entry in st.session_state.chat_history:
    st.write(f"**User:** {entry['question']}")
    st.write(f"**Response:** {entry['response']}")

# Process user input and display responses
if user_question:
    if model_choice == "Groq":
        response = get_groq_response(user_question)
    else:
        response = get_lm_studio_response(user_question)

    st.session_state.chat_history.append({
        "question": user_question,
        "response": response
    })
