"""
To run the dashboard, use the following command in the terminal:
`streamlit run app.py`
"""
from source import APIClient
import streamlit as st

st.title("RFP Question Answering Interface")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please submit a question"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

client = APIClient("http://localhost:8081")

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.inference(prompt, return_count=1)
    if not response.answers:
        message = "I'm sorry, I don't have an answer to that question."
        st.session_state.messages.append({"role": "assistant", "content": message})
        st.chat_message("assistant").write(message)
    for answer in response.answers:
        message = message.text
        st.session_state.messages.append({"role": "assistant", "content": message})
        st.chat_message("assistant").write(message)
