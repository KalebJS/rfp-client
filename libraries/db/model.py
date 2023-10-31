from typing import Optional

from sqlmodel import Field, SQLModel


class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    linked_org: Optional[str] = None


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    answer_id: Optional[int] = Field(default=None, foreign_key="answer.id")


class APIToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token_hash: str
