import os
import requests
import time
from dotenv import load_dotenv

# ===============================
# STEP 1: Load .env file
# ===============================
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not groq_api_key or not gemini_api_key:
    print("ERROR: API keys not found in .env file")
    exit()

# ===============================
# STEP 2: Take user input
# ===============================
user_prompt = input("Enter your prompt: ")

# ===============================
# STEP 3: GROQ REST API CALL
# ===============================
groq_url = "https://api.groq.com/openai/v1/chat/completions"

groq_headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}

groq_payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

groq_start = time.time()
groq_response = requests.post(
    groq_url,
    headers=groq_headers,
    json=groq_payload
)
groq_time = time.time() - groq_start

if groq_response.status_code == 200:
    groq_text = groq_response.json()["choices"][0]["message"]["content"]
else:
    groq_text = f"Groq API Error: {groq_response.text}"

# ===============================
# STEP 4: GEMINI REST API CALL (FIXED)
# ===============================
gemini_url = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-1.5-flash:generateContent"
    f"?key={gemini_api_key}"
)

gemini_payload = {
    "contents": [
        {
            "parts": [
                {"text": user_prompt}
            ]
        }
    ]
}

gemini_start = time.time()
gemini_response = requests.post(
    gemini_url,
    headers={"Content-Type": "application/json"},
    json=gemini_payload
)
gemini_time = time.time() - gemini_start

gemini_json = gemini_response.json()

if "candidates" in gemini_json:
    gemini_text = gemini_json["candidates"][0]["content"]["parts"][0]["text"]
else:
    gemini_text = f"Gemini API Error: {gemini_json}"

# ===============================
# STEP 5: OUTPUT & COMPARISON
# ===============================
print("\n================ GROQ RESPONSE ================")
print(groq_text)
print("Time Taken:", round(groq_time, 3), "seconds")

print("\n=============== GEMINI RESPONSE ===============")
print(gemini_text)
print("Time Taken:", round(gemini_time, 3), "seconds")

print("\n=============== SPEED COMPARISON ===============")
if groq_time < gemini_time:
    print("Groq is faster than Gemini")
elif gemini_time < groq_time:
    print("Gemini is faster than Groq")
else:
    print("Both have similar response time")
print("===============================================")