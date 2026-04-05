import streamlit as st
from chroma_setup import create_vector_db
from rag_pipeline import ask_hr_bot

# ------------------ CONFIG ------------------
st.set_page_config(page_title="HR Chatbot", page_icon="💬", layout="centered")

# ------------------ INIT ------------------
@st.cache_resource
def init():
    collection = create_vector_db()
    return collection

collection = init()

# Replace with your actual key or use st.secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ UI HEADER ------------------
st.title("💬 HR Policy Chatbot")
st.caption("Ask questions about HR policies")

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ INPUT ------------------
if prompt := st.chat_input("Ask your HR question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask_hr_bot(prompt, collection, api_key)
            except Exception as e:
                response = f"❌ Error: {str(e)}"

        st.markdown(response)

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Options")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This is an AI HR chatbot using RAG + Groq.")
