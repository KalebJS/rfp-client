"""
To run the dashboard, use the following command in the terminal:
`streamlit run dashboard.py`
"""
import streamlit as st
import pandas as pd
from libraries.db import DatabaseProxy


db = DatabaseProxy()

questions = db.get_questions()
df_questions = pd.DataFrame([dict(q) for q in questions])
df_questions.drop(columns=["_sa_instance_state"], inplace=True)

answers = db.get_answers()
df_answers = pd.DataFrame([dict(a) for a in answers])
df_answers.drop(columns=["_sa_instance_state"], inplace=True)

users = db.get_users()
df_users = pd.DataFrame([dict(u) for u in users])
df_users.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")

organizations = db.get_organizations()
df_organizations = pd.DataFrame([dict(o) for o in organizations])
df_organizations.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")


st.title("Dashboard")

st.subheader("Questions")
st.write(f"Total: {len(df_questions)}")
st.write(df_questions)

st.subheader("Answers")
st.write(f"Total: {len(df_answers)}")
st.write(df_answers)

st.subheader("Users")
st.write(f"Total: {len(df_users)}")
st.write(df_users)

st.subheader("Organizations")
st.write(f"Total: {len(df_organizations)}")
st.write(df_organizations)