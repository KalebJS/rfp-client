"""
To run the dashboard, use the following command in the terminal:
`streamlit run app.py`
"""
import pandas as pd
import streamlit as st

from libraries.st_utils import get_db

db = get_db()


tables = {"questions": db.get_questions, "answers": db.get_answers, "users": db.get_users, "organizations": db.get_organizations}
primary_table = st.selectbox("Table", tables.keys())

items = tables[primary_table]()
df = pd.DataFrame([dict(o) for o in items])
df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")

st.subheader(f"{primary_table.capitalize()} Table")
st.write(f"Total: {len(df)}")
st.dataframe(df, hide_index=True)
