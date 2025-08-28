import streamlit as st
import requests

st.title("Agentic AI Chat (Streamlit + FastAPI + LangGraph)")

if "history" not in st.session_state:
    st.session_state.history = []  # keep chat memory in Streamlit

question = st.text_input("Ask the AI:")

if st.button("Send"):
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
