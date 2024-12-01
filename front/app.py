import time
import streamlit as st

from chat import chat_llm
from login import login


API_BASE_URL = "http://127.0.0.1:8000/api" # FastAPI 서버의 URL

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login(API_BASE_URL)
else:
    chat_llm(API_BASE_URL)