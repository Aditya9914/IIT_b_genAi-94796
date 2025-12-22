import os
import pandas as pd
import streamlit as st
from pandasql import sqldf
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

st.set_page_config(page_title="CSV SQL Explorer", layout="wide")
st.title("📊 CSV Explorer with LLM-powered SQL")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview of Data")
    st.dataframe(df.head())

    st.subheader("🧩 CSV Schema")
    st.write(df.dtypes)

    question = st.text_input(
        "Ask a question about this CSV (use table name `data`):"
    )

    if st.button("Run Query") and question:
        with st.spinner("Thinking..."):
            # Prompt for SQL generation
            prompt = f"""
You are an expert SQL assistant.

Table name: data
Table schema:
{df.dtypes}

User question:
{question}

Instructions:
1. Write ONLY a valid SQLite SQL query.
2. Do NOT include explanations.
3. Use table name `data`.
"""

            sql_response = llm.invoke(prompt)
            sql_query = sql_response.content.strip()

            try:
                # Execute SQL
                result_df = sqldf(sql_query, {"data": df})

                # Explain result
                explanation_prompt = f"""
Explain the following query result in very simple English.

Result:
{result_df.head(10)}
"""
                explanation = llm.invoke(explanation_prompt).content

                # Save to history
                st.session_state.history.append({
                    "question": question,
                    "sql": sql_query,
                    "result": result_df,
                    "explanation": explanation
                })

            except Exception as e:
                st.error(f"❌ Error executing SQL: {e}")

    # Display query history (LOOP)
    if st.session_state.history:
        st.subheader("🕒 Query History")

        for i, item in enumerate(st.session_state.history, start=1):
            st.markdown(f"### 🔹 Query {i}")
            st.markdown(f"**Question:** {item['question']}")

            st.markdown("**Generated SQL:**")
            st.code(item["sql"], language="sql")

            st.markdown("**Result:**")
            st.dataframe(item["result"])

            st.markdown("**Explanation:**")
            st.write(item["explanation"])

            st.divider()
