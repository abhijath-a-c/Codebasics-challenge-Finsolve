import streamlit as st

st.set_page_config(page_title="Company RAG Chatbot", page_icon="💬", layout="centered")

st.title("Welcome to Company RAG Chatbot 🤖")

st.markdown("""
Department-specific answers using **Retrieval-Augmented Generation (RAG)**.

- 🔐 Login to continue
- 🗂️ Role-based data access
""")

if st.button("🔑 Login"):
    st.switch_page("pages/1_Login.py")
