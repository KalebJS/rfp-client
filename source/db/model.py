from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Field, SQLModel


class Table(SQLModel):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_onupdate=text("CURRENT_TIMESTAMP"),
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


class Organization(Table, table=True):
    name: str
    description: Optional[str] = None


class User(Table, table=True):
    first_name: str
    last_name: str
    organization: str


class Answer(Table, table=True):
    text: str
    owner_organization: int = Field(default=None, foreign_key="organization.id")


class Question(Table, table=True):
    text: str
    is_active: bool = True
    answer_id: Optional[int] = Field(default=None, foreign_key="answer.id")


class APIToken(Table, table=True):
    token_hash: str
