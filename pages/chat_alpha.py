import streamlit as st

from libraries.db import DatabaseProxy
from libraries.index_proxy import IndexProxy


if "db" not in st.session_state:
    db = DatabaseProxy()
    st.session_state["db"] = db
else:
    db = st.session_state["db"]

if "index" not in st.session_state:
    index = IndexProxy(db, verbose=True)
    index.reset()
    st.session_state["index"] = index
else:
    index = st.session_state["index"]

st.title("RFP Question Answering Interface") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please submit a question"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


def add_assistant_message(text: str):
    st.session_state.messages.append({"role": "assistant", "content": text})


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    answers = index.inference(prompt, return_count=1)
    for answer_id, score in answers:
        answer = db.get_answer_by_id(answer_id)
        answer = answer.text
        # answer = f"{answer_id} {round(score, 2)}: {answer.text}"
        add_assistant_message(answer)
        st.chat_message("assistant").write(answer)
    