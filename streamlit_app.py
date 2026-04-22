import streamlit as st
import datetime
import requests
import sys

BASE_URL = "http://localhost:8000" # backend url

st.set_page_config(
    page_title="Travel Planner Agentic Application",
    page_icon="🌴",
    layout="centerd",
    initial_sidebar_state="expanded",
)

st.title("AI Travel Agent")

# initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("How can I help you? Let me know your travel destination.")

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g., Plan a 5 day trip to Paris")
    submit_button = st.form_submit_button("Submit")

if submit_button and user_input.strip():
    try:
        with st.spinner("AI Travel Agent is planning your trip..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "I'm sorry, I don't have an answer for that.")

            markdown_content = f"""
            ## AI Travel Agent's Summary for the trip:

            ---

            {answer}

            ---

            ### Thank you for using AI Travel Agent.
            #### Created at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            """
            st.markdown(markdown_content, unsafe_allow_html=True)

    except Exception as e:
        raise f"The response from AI Travel Agent is not valid: {e}"
