import streamlit as st
import time

st.set_page_config(page_title="Chat Bot", layout="wide")
st.title("My ChatBot")

# ---------------- Initialize session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("📌 Sidebar")

    # 1️⃣ History
    st.subheader("🕘 History")
    if st.session_state.messages:
        for role, msg in st.session_state.messages:
            st.write(f"{role.capitalize()}: {msg}")
    else:
        st.write("No chat history yet.")

    if st.button("🗑 Clear History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # 2️⃣ ChatGPT related info
    st.subheader("🤖 ChatGPT Info")
    st.write("""
    - ChatGPT is an AI chatbot  
    - Built using Large Language Models (LLMs)  
    - Can answer questions & chat naturally  
    - Used in apps, assistants & chat systems  
    """)

# ---------------- Display chat history ----------------
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# ---------------- User Input ----------------
user_input = st.chat_input("Type your message")

if user_input:
    # Store user message
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Bot reply (fake for demo)
    bot_reply = f"You said: {user_input}"

    # Generator for streaming bot reply with delay
    def stream_reply(text):
        for word in text.split():
            yield word + " "
            time.sleep(0.3)  # typing effect

    # Display bot reply with streaming effect
    with st.chat_message("assistant"):
        st.write_stream(stream_reply(bot_reply))

    # Save bot reply in session history
    st.session_state.messages.append(("assistant", bot_reply))
