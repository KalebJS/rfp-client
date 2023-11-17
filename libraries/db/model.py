from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, Column, text

from sqlmodel import Field, SQLModel


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    organization: str
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))
    )


class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    owner_organization: int = Field(default=None, foreign_key="organization.id")
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))
    )


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_active: bool = True
    answer_id: Optional[int] = Field(default=None, foreign_key="answer.id")
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))
    )


class APIToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token_hash: str
    created_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    modified_datetime: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text("CURRENT_TIMESTAMP"))
    )
