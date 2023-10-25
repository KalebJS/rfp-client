from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from .model import Answer


class DatabaseProxy:
    def __init__(self):
        self.engine = self.create_db_and_tables()

    def create_db_and_tables(self):
        database_file_path = Path("instance/database.sqlite")
        database_file_path.parent.mkdir(parents=True, exist_ok=True)
        sqlite_url = f"sqlite:///{database_file_path}"
        engine = create_engine(sqlite_url)
        SQLModel.metadata.create_all(engine)
        return engine

    def get_answer_by_id(self, id: int) -> str:
        with Session(self.engine) as session:
            answer = session.get(Answer, id)
            return answer.text

