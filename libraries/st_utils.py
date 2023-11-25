import pandas as pd
import streamlit as st

from libraries.db.database import DatabaseProxy
from libraries.index_proxy import IndexProxy


def get_db() -> DatabaseProxy:
    if "db" not in st.session_state:
        db = DatabaseProxy()
        st.session_state["db"] = db
    return st.session_state["db"]


def get_index() -> IndexProxy:
    db = get_db()
    if "index" not in st.session_state:
        index = IndexProxy(db, verbose=True)
        index.reset()
        st.session_state["index"] = index
    return st.session_state["index"]


def export_database():
    db = get_db()
    questions = db.get_questions()
    questions = [q.dict() for q in questions]
    df_questions = pd.DataFrame(questions)

    answers = db.get_answers()
    answers = [a.dict() for a in answers]
    df_answers = pd.DataFrame(answers)

    users = db.get_users()
    users = [a.dict() for a in users]
    df_users = pd.DataFrame(users)

    organizations = db.get_organizations()
    organizations = [a.dict() for a in organizations]
    df_organizations = pd.DataFrame(organizations)

    output_path = "output/export.xlsx"
    # combine as different sheets in excel
    with pd.ExcelWriter(output_path) as writer:
        df_questions.to_excel(writer, sheet_name="questions", index=False)
        df_answers.to_excel(writer, sheet_name="answers", index=False)
        df_users.to_excel(writer, sheet_name="users", index=False)
        df_organizations.to_excel(writer, sheet_name="organizations", index=False)
    
    return output_path
