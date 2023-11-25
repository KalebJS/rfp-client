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
