# -------------------------------
# 🌾 Farmer Assistant UI (Improved)
# -------------------------------
API_URL = "https://agri-assistancebot-backend.onrender.com/ask"
import streamlit as st
import requests

st.set_page_config(page_title="Farmer Assistant", layout="wide")

st.title("🌾 Farmer Assistant")

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# SIDEBAR (CHAT HISTORY)
# -------------------------------
with st.sidebar:
    st.header("💬 Chat History")

    for i, chat in enumerate(st.session_state.history):
        if st.button(chat[:30] + "...", key=i):
            st.session_state.messages = chat

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []

# -------------------------------
# DISPLAY CHAT (ChatGPT style)
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# INPUT BOX (ChatGPT style)
# -------------------------------
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------
    # STREAM RESPONSE FROM FASTAPI
    # -------------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        with requests.post(
            API_URL,
            json={"question": user_input},
            stream=True
        ) as r:

            for chunk in r.iter_content(chunk_size=10):
                if chunk:
                    text = chunk.decode("utf-8")
                    full_text += text
                    placeholder.markdown(full_text + "▌")

        placeholder.markdown(full_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_text
    })
