import pandas as pd
import streamlit as st

from libraries.db.model import Answer, Question
from libraries.st_utils import get_db

st.title("Table Reset")

uploaded_file = st.file_uploader("Input file", "csv")

with st.sidebar:
    encoding = st.text_input("Encoding", "latin-1")

if not st.button("Run"):
    st.stop()
if not uploaded_file or not encoding:
    st.error("Please make sure all fields are filled out.")
    st.stop()

df = pd.read_csv(uploaded_file, encoding="latin-1", dtype="str")


db = get_db()
db.delete_questions_answers()

for _, row in df.iterrows():
    answer = Answer(text=str(row["answer"]).strip())
    answer = db.insert_answer(answer)
    question = Question(text=str(row["question"]).strip(), answer_id=answer.id)
    db.insert_question(question)
