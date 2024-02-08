from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Tuple

import chromadb
from libraries.db import DatabaseProxy, Question


@dataclass
class IndexItem:
    question_id: int
    score: float


class IndexProxy:
    def __init__(self, database: DatabaseProxy, name: str = "vector_database", verbose: bool = False):
        self.db = database
        self.verbose = verbose

        chroma_client = chromadb.PersistentClient("./instance")
        self.collection = chroma_client.create_collection(name=name, get_or_create=True, metadata={"hnsw:space": "ip"})

    def reset(self) -> None:
        if self.collection.count():
            ids = self.collection.get()["ids"]
            self.collection.delete(ids)

        questions = self.db.get_questions()

        documents = [q.text for q in questions]
        metadatas = [{"id": q.id} for q in questions]
        ids = [str(q.id) for q in questions]

        self.collection.add(ids, metadatas=metadatas, documents=documents)

        if self.verbose:
            print("INFO", f"Inserted {len(questions)} into index")

    def add(self, question: Question):
        self.collection.add(ids=[question.id], metadatas=[{"id": question.id}], documents=[question.text])

    def print_results(self, results: List[IndexItem]):
        for item in results:
            question = self.db.get_question_by_id(item.question_id)
            print(f"Answer ID: {question.answer_id}—Score: {item.score}—Text: `{question.text}`")

    def nearest_neighbors(self, results: List[IndexItem]) -> List[Tuple[int, float]]:
        classes = defaultdict(int)
        for item in results:
            question = self.db.get_question_by_id(item.question_id)
            score = 1 - item.score
            classes[question.answer_id] += score

        if self.verbose:
            print(dict(classes))

        # create list of tuples (score, class) and sort it
        sorted_classes = sorted(classes.items(), key=lambda x: x[1], reverse=True)
        return sorted_classes

    def query(self, query: str, k: Optional[int] = 10, threshold: float = float("inf")) -> List[IndexItem]:
        if k > self.collection.count():
            raise ValueError(f"Your index has size {self.collection.count} but you set n_results to {k}.")
        query_results = self.collection.query(query_texts=[query], n_results=k)
        results = []
        for i in range(k):
            item = IndexItem(question_id=query_results["ids"][0][i], score=query_results["distances"][0][i])
            if item.score > threshold:
                break
            results.append(item)

        if self.verbose:
            self.print_results(results)

        return results

    def inference(
        self, query: str, k: Optional[int] = 10, return_count: Optional[int] = 1, threshold: float = float("inf")
    ) -> List[Tuple[int, float]]:
        results = self.query(query, k=k, threshold=threshold)

        relevant_answers = self.nearest_neighbors(results)
        top_answers = relevant_answers[:return_count]
        return top_answers

    def __sizeof__(self) -> int:
        return self.collection.count()
