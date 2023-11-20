"""
To run the dashboard, use the following command in the terminal:
` where do I print?`
"""
import pandas as pd
import streamlit as st

from libraries.db import DatabaseProxy

db = DatabaseProxy()

questions = db.get_questions()
df_questions = pd.DataFrame([dict(q) for q in questions])
df_questions.drop(columns=["_sa_instance_state", "is_active", "created_datetime", "modified_datetime"], inplace=True)

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
st.dataframe(df_questions, hide_index=True)

st.subheader("Answers")
st.write(f"Total: {len(df_answers)}")
st.dataframe(df_answers, hide_index=True)

st.subheader("Users")
st.write(f"Total: {len(df_users)}")
st.dataframe(df_users, hide_index=True)

st.subheader("Organizations")
st.write(f"Total: {len(df_organizations)}")
st.dataframe(df_organizations, hide_index=True)
