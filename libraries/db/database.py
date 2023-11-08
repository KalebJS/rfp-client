from pathlib import Path
from uuid import uuid4

from sqlmodel import Session, SQLModel, create_engine

from .model import APIToken, Answer, Question


class DatabaseProxy:
    def __init__(self, reset: bool = False):
        self.engine = self.create_db_and_tables(reset)

    def create_db_and_tables(self, reset: bool = False):
        database_file_path = Path("instance/database.sqlite")
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
