import streamlit as st
import requests

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_thanks" not in st.session_state:
    st.session_state.show_thanks = False

# ---------------- LOGIN PAGE ----------------
def login_page():
    if st.session_state.show_thanks:
        st.success("🙏 Thanks for visiting our site...")
        st.session_state.show_thanks = False

    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Email must end with .com
        email_valid = email.endswith(".com")

        # Password must contain at least 4 digits
        digits_count = sum(char.isdigit() for char in password)
        password_valid = digits_count >= 4

        if email_valid and password_valid:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Email must end with .com and password must contain at least 4 numbers")

# ---------------- WEATHER PAGE ----------------
def weather_page():
    api_key = "10575925b2f79fb195fad9ad6ca12654"

    st.title("🌤️ Weather App")

    city = st.text_input("Enter city name")

    if st.button("Get Weather"):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather = response.json()

        if response.status_code == 200:
            condition = weather["weather"][0]["main"]

            icons = {
                "Clear": "☀️",
                "Clouds": "☁️",
                "Rain": "🌧️",
                "Thunderstorm": "⛈️",
                "Snow": "❄️",
                "Mist": "🌫️"
            }

            icon = icons.get(condition, "🌤️")

            st.subheader(f"{icon} {condition}")
            st.write(f"🌡️ Temperature: {weather['main']['temp']} °C")
            st.write(f"💧 Humidity: {weather['main']['humidity']} %")
            st.write(f"🌬️ Wind Speed: {weather['wind']['speed']} m/s")
        else:
            st.error(weather.get("message", "City not found"))

    st.markdown("---")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.show_thanks = True
        st.rerun()

# ---------------- MAIN ROUTER ----------------
if st.session_state.logged_in:
    weather_page()
else:
    login_page()
