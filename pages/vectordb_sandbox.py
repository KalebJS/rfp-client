import pandas as pd
import streamlit as st
from libraries.db import DatabaseProxy
from libraries.index_proxy import IndexProxy
from libraries.st_utils import get_db, get_index

db = get_db()
index = get_index()

with st.sidebar:
    st.slider("k", 1, 20, 7, 1, key="k")


st.title("Index Proxy")
if prompt := st.text_input("Enter a string"):
    items = index.query(prompt, k=st.session_state["k"])

    rows = []
    for item in items:
        question = db.get_question_by_id(item.question_id)
        rows.append([question.id, question.answer_id, question.text, item.score])

    df = pd.DataFrame(rows, columns=["Question ID", "Answer ID", "Question Text", "Score"])
    st.dataframe(df)

    st.write("Nearest neighbors")

    neighbors = index.nearest_neighbors(items)
    rows = []
    for answer_id, score in neighbors:
        answer = db.get_answer_by_id(answer_id)
        rows.append([answer_id, score, answer.text])

    df = pd.DataFrame(rows, columns=["Answer ID", "Score", "Answer Text"])
    st.dataframe(df)
