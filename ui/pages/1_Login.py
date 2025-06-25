import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

API_URL = "http://127.0.0.1:8000"  # Should match FastAPI backend

st.set_page_config(page_title="🔐 Login - FinSolve IQ", layout="centered")
st.title("🔑 Login to FinSolve IQ")

# Initialize session state on first load
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login Form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        if not username or not password:
            st.warning("⚠️ Please provide both username and password.")
        else:
            try:
                response = requests.post(f"{API_URL}/login", auth=HTTPBasicAuth(username, password))
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.role = data.get("role", "unknown")
                    st.session_state.messages = []  # Reset chat history for new session
                    st.success("✅ Login successful! Redirecting...")
                    st.switch_page("pages/2_Chat.py")  # ✅ Ensure this matches your actual file path/name
                else:
                    st.error(f"❌ Login failed: {response.json().get('detail', 'Invalid credentials')}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")

# Redirect if already logged in (e.g., after page reload)
if st.session_state.get("logged_in", False):
    st.switch_page("pages/2_Chat.py")
