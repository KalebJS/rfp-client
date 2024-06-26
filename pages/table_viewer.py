import pandas as pd
import streamlit as st
from source.st_utils import export_database, get_db

db = get_db()


with st.sidebar:
    fp = export_database()
    with open(fp, "rb") as f:
        st.download_button("Export Database", f, "database.xlsx")


tables = {
    "questions": db.get_questions,
    "answers": db.get_answers,
    "users": db.get_users,
    "organizations": db.get_organizations,
}
primary_table = st.selectbox("Table", tables.keys())

items = tables[primary_table]()
df = pd.DataFrame([dict(o) for o in items])
df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")

st.subheader(f"{primary_table.capitalize()} Table")
st.write(f"Total: {len(df)}")
st.dataframe(df, hide_index=True)
