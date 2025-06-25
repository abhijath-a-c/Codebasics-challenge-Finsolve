import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import os

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="💬 FinSolve IQ - Intelligent Chatbot", layout="centered")

if not st.session_state.get("logged_in", False):
    st.error("❌ You must log in first.")
    st.switch_page("pages/1_Login.py")

st.title("💬 FinSolve IQ - Intelligent RAG Chatbot")
st.caption(f"Logged in as **{st.session_state.username}** | Role: `{st.session_state.role}`")

def chat_with_backend(question):
    payload = {"question": question}
    response = requests.post(
        f"{API_URL}/chat",
        json=payload,
        auth=HTTPBasicAuth(st.session_state.username, st.session_state.password)
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"❌ Error {response.status_code}: {response.text}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("source"):
            with st.expander(f"Source: {msg['source'].get('source', 'Unknown')}"):
                st.markdown(msg["source"].get("content", ""))

with st.sidebar:
    st.markdown("📂 **Upload New Document**")
    uploaded_file = st.file_uploader("Choose a .md or .csv file", type=["md", "csv"])

    if uploaded_file:
        if st.session_state.role == "c-level":
            dept_choice = st.selectbox("Select Department to Upload To:", ["finance", "marketing", "hr", "engineering"])
        else:
            dept_choice = st.session_state.role

        if st.button("Upload & Process"):
            with st.spinner("Uploading file and processing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/upload",
                        auth=HTTPBasicAuth(st.session_state.username, st.session_state.password),
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                        data={"target_department": dept_choice}
                    )
                    if response.status_code == 200:
                        st.success(response.json().get("message", "✅ Upload success."))
                    else:
                        st.error(f"❌ Upload failed: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ Upload error: {e}")

if question := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Thinking... 🤔"):
        response = chat_with_backend(question)

    if "error" in response:
        assistant_msg = response["error"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        with st.chat_message("assistant"):
            st.markdown(assistant_msg)
    else:
        answer = response.get("answer", "⚠️ No answer received.")
        sources = response.get("sources", [])
        top_source = sources[0] if sources else None

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "source": top_source if sources else None
        })

        with st.chat_message("assistant"):
            st.markdown(answer)
            if sources:
                for src in sources:
                    with st.expander(f"{src.get('source', 'Unknown Source')}"):
                        st.markdown(src.get("content", ""))
            else:
                with st.expander("No Source Available ❗"):
                    st.markdown("_No source information returned from backend._")

if st.button("🔓 Logout"):
    for key in ["logged_in", "username", "password", "role", "messages"]:
        st.session_state.pop(key, None)
    st.switch_page("pages/1_Login.py")
