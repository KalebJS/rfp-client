from pathlib import Path
from uuid import uuid4

import pandas as pd
from sqlalchemy import delete
from sqlmodel import Session, SQLModel, create_engine

from .model import Answer, APIToken, Organization, Question, User


class DatabaseProxy:
    def __init__(self, reset: bool = False, database: str = "database"):
        self.engine = self.create_db_and_tables(reset, database)

    def create_db_and_tables(self, reset: bool, database: str):
        database_file_path = Path(f"instance/{database}.sqlite")
        database_file_path.parent.mkdir(parents=True, exist_ok=True)
        sqlite_url = f"sqlite:///{database_file_path}"
        engine = create_engine(sqlite_url)
        if reset:
            SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        return engine

    def get_answer_by_id(self, id: int) -> str:
        with Session(self.engine) as session:
            answer = session.get(Answer, id)
            return answer

    def insert_from_dataframe(self, df: pd.DataFrame, col_questions: str, col_answers: str) -> None:
        for _, row in df.iterrows():
            answer = Answer(text=str(row[col_answers]).strip())
            answer = self.insert_answer(answer)
            question = Question(text=str(row[col_questions]).strip(), answer_id=answer.id)
            self.insert_question(question)

    def insert_answer(self, answer: Answer):
        with Session(self.engine) as session:
            session.add(answer)
            session.commit()
            session.refresh(answer)
            return answer

    def insert_question(self, question: Question):
        with Session(self.engine) as session:
            session.add(question)
            session.commit()
            session.refresh(question)
            return question

    def get_question_by_id(self, id: int) -> str:
        with Session(self.engine) as session:
            question = session.get(Question, id)
            return question

    def create_api_token(self):
        token = uuid4().hex
        token_hash = hash(token)
        with Session(self.engine) as session:
            api_token = APIToken(token_hash=token_hash)
            session.add(api_token)
            session.commit()
            session.refresh(api_token)
            return token

    def validate_token(self, token: str) -> bool:
        with Session(self.engine) as session:
            token_hash = hash(token)
            api_token = session.get(APIToken, token_hash)
            return api_token is not None

    def get_questions(self):
        with Session(self.engine) as session:
            return session.query(Question).all()

    def get_answers(self):
        with Session(self.engine) as session:
            return session.query(Answer).all()

    def get_users(self):
        with Session(self.engine) as session:
            return session.query(User).all()

    def get_organizations(self):
        with Session(self.engine) as session:
            return session.query(Organization).all()

    def delete_questions_answers(self):
        with Session(self.engine) as session:
            stmt = delete(Question)
            session.execute(stmt)
            stmt = delete(Answer)
            session.execute(stmt)
            session.commit()
