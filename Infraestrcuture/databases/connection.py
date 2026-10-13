from os import getenv
from Infraestrcuture.databases.base import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from Infraestrcuture.utils.utils import Singleton

load_dotenv()


class DatabaseConnection(metaclass=Singleton):
    base = Base

    engine: Engine
    session_factory: sessionmaker

    def establish_connection(self):
        postgresql_url = getenv("POSTGRESQL_URL")

        if not postgresql_url:
            raise ValueError(
                "A variável POSTGRESQL_URL não foi encontrada no .env"
            )

        self.engine = create_engine(postgresql_url)

    def generate_database_schema(self):
        self.base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        return self.session_factory()

    def configure_session_factory(self):
        self.session_factory = sessionmaker(bind=self.engine)
