import requests
import streamlit as st


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please submit a question"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


def add_assistant_message(text: str):
    st.session_state.messages.append({"role": "assistant", "content": text})

url = "http://localhost:8000/inference/"

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    payload = {"question": prompt}
    response = requests.post(url, json=payload)
    answers = response.json()
    for answer in answers:
        add_assistant_message(answer["answer"])
        st.chat_message("assistant").write(answer["answer"])