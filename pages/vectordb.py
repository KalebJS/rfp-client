from collections import defaultdict
import streamlit as st
import chromadb

from libraries.db import DatabaseProxy

db = DatabaseProxy()

chroma_client = chromadb.PersistentClient("./instance")
collection = chroma_client.create_collection(
    name="my_collection", get_or_create=True, metadata={"hnsw:space": "ip"}
)


def nearest_neighbors(results):
    classes = defaultdict(int)
    for i in range(len(results["ids"][0])):
        question = db.get_question_by_id(results["ids"][0][i])
        score = 1 - round(results["distances"][0][i], 2)
        classes[question.answer_id] += score
        
    st.write(dict(classes))

    return max(classes, key=classes.get)

def print_results(results):
    for i in range(len(results["ids"][0])):
        question = db.get_question_by_id(results["ids"][0][i])
        st.write(round(results["distances"][0][i], 2), question.answer_id, results["documents"][0][i])

query = st.text_input("Query")
n_results = st.number_input("Number of results", min_value=1, max_value=100, value=10)
if query:
    results = collection.query(query_texts=[query], n_results=n_results)
    print_results(results)
    st.write(nearest_neighbors(results))

    