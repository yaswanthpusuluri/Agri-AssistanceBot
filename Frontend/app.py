# -------------------------------
# 🌾 Farmer Assistant UI (Fixed)
# -------------------------------

import streamlit as st
import requests

API_URL = "https://agri-assistancebot-backend.onrender.com/ask"

st.set_page_config(page_title="Farmer Assistant", layout="wide")

st.title("🌾 Farmer Assistant")

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# DISPLAY CHAT
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# INPUT
# -------------------------------
user_input = st.chat_input("Ask your question...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        try:
            r = requests.post(
                API_URL,
                json={"question": user_input},
                timeout=60
            )

            if r.status_code == 200:
                full_text = r.json().get("answer", "")
            else:
                full_text = f"Error: {r.status_code}"

        except Exception as e:
            full_text = f"⚠️ Server error: {e}"

        placeholder.markdown(full_text)

    # save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_text
    })
