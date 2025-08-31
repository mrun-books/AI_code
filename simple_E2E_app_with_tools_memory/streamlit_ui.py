import streamlit as st
import requests

st.title("AI Content Marketing Assistant ")

if "history" not in st.session_state:
    st.session_state.history = []  # keep chat memory in Streamlit

question = st.chat_input("Ask the AI:")

if question:
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state.history = data["history"]  # overwrite with backend history
    else:
        st.error("Error calling backend")

# Render chat history
for msg in st.session_state.history:
    if msg["role"] == "human":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")
