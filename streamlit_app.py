import streamlit as st
import datetime
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Voyage — AI Travel Concierge",
    page_icon="✈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #07091a !important;
    font-family: 'Nunito Sans', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 45% at 50% -5%, rgba(201,168,76,0.11) 0%, transparent 65%),
        radial-gradient(ellipse 55% 55% at 90% 110%, rgba(14,28,70,0.6) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer { visibility: hidden; }
.stDeployButton, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.main .block-container {
    max-width: 700px;
    padding: 0 2rem 5rem;
}

/* ── Header ── */
.voyage-header {
    text-align: center;
    padding: 4.5rem 0 3rem;
}

.voyage-wordmark {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5.5rem;
    font-weight: 300;
    font-style: italic;
    color: #c9a84c;
    letter-spacing: 0.06em;
    line-height: 1;
    text-shadow: 0 0 70px rgba(201,168,76,0.28);
}

.voyage-sub {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.62rem;
    font-weight: 400;
    letter-spacing: 0.55em;
    text-transform: uppercase;
    color: rgba(245,240,232,0.35);
    margin-top: 0.6rem;
}

.ornament {
    color: rgba(201,168,76,0.45);
    font-size: 1rem;
    letter-spacing: 0.6rem;
    margin: 1.8rem 0 0;
}

/* ── Form card ── */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(201,168,76,0.18) !important;
    border-radius: 1px !important;
    padding: 2.2rem 2.6rem !important;
    box-shadow: 0 14px 55px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,168,76,0.07) !important;
}

[data-testid="stForm"] label p,
.stTextInput label {
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.38em !important;
    text-transform: uppercase !important;
    color: rgba(201,168,76,0.62) !important;
}

.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(201,168,76,0.22) !important;
    border-radius: 0 !important;
    color: #f5f0e8 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.3rem !important;
    font-weight: 300 !important;
    padding: 0.6rem 0 !important;
    caret-color: #c9a84c !important;
    box-shadow: none !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}

.stTextInput > div > div > input:focus {
    border-bottom-color: #c9a84c !important;
    box-shadow: 0 1px 0 rgba(201,168,76,0.45) !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(245,240,232,0.18) !important;
    font-style: italic !important;
    font-weight: 300 !important;
}

.stFormSubmitButton > button {
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.55) !important;
    color: #c9a84c !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.42em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 3rem !important;
    border-radius: 0 !important;
    margin-top: 1.6rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
}

.stFormSubmitButton > button:hover {
    background: rgba(201,168,76,0.1) !important;
    border-color: #c9a84c !important;
    box-shadow: 0 0 28px rgba(201,168,76,0.14) !important;
    color: #ddb84e !important;
}

.stFormSubmitButton > button:active {
    transform: scale(0.99) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    border-top-color: #c9a84c !important;
}

/* ── Response card ── */
.response-wrap {
    margin-top: 2.2rem;
    border: 1px solid rgba(201,168,76,0.14);
    border-top: 2px solid #c9a84c;
    background: rgba(255,255,255,0.022);
    box-shadow: 0 10px 45px rgba(0,0,0,0.38);
    padding: 2.5rem 2.6rem;
}

.response-label {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.45em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 0.4rem;
}

.response-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 300;
    color: #f5f0e8;
    margin-bottom: 1.4rem;
    line-height: 1.1;
}

.response-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(201,168,76,0.38), transparent);
    margin-bottom: 1.6rem;
}

.response-body {
    font-family: 'Nunito Sans', sans-serif;
    color: rgba(245,240,232,0.80);
    font-size: 0.9rem;
    line-height: 1.9;
    font-weight: 300;
    white-space: pre-wrap;
}

.response-footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(201,168,76,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.response-footer-brand {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 0.88rem;
    color: rgba(201,168,76,0.45);
}

.response-footer-time {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 0.6rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    color: rgba(245,240,232,0.22);
}

/* ── Error ── */
.stAlert {
    background: rgba(180,50,50,0.1) !important;
    border: 1px solid rgba(180,50,50,0.22) !important;
    border-radius: 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.22); }
::-webkit-scrollbar-thumb:hover { background: rgba(201,168,76,0.45); }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="voyage-header">
    <div class="voyage-wordmark">Voyage</div>
    <div class="voyage-sub">AI Travel Concierge</div>
    <div class="ornament">— ✦ —</div>
</div>
""",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Destination & Details",
        placeholder="e.g., Plan a 5 day trip to Paris in spring…",
    )
    submit_button = st.form_submit_button("Plan My Journey")

if submit_button and user_input.strip():
    try:
        with st.spinner("Crafting your bespoke itinerary…"):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No itinerary was returned.")
            timestamp = datetime.datetime.now().strftime("%B %d, %Y · %H:%M")

            st.markdown(
                f"""
<div class="response-wrap">
    <div class="response-label">Your Itinerary</div>
    <div class="response-title">Travel Plan</div>
    <div class="response-divider"></div>
    <div class="response-body">{answer}</div>
    <div class="response-footer">
        <span class="response-footer-brand">Voyage</span>
        <span class="response-footer-time">{timestamp}</span>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(
            "Unable to reach the travel concierge. Please ensure the backend service is running."
        )
