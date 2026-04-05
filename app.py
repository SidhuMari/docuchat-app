import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

import streamlit as st
from chroma_setup import create_vector_db
from rag_pipeline import ask_hr_bot

st.set_page_config(page_title="DocuChat HR Bot")

st.title("🤖 HR Policy Chatbot")

# Load DB
collection = create_vector_db()

# API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Chat UI
user_input = st.text_input("Ask your HR question:")

if user_input:
    answer = ask_hr_bot(user_input, collection, api_key)
    st.write("🤖", answer)
