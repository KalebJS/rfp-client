from typing import List
from pydantic import BaseModel


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str
    score: float


class InferenceResponse(BaseModel):
    answers: List[Answer]
    