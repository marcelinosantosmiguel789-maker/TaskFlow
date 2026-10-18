
from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from Infraestrcuture.databases.base import Base

load_dotenv()


class DatabaseConnection:
    base = Base

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url
        self.engine: Engine | None = None
        self.session_factory: sessionmaker | None = None

    def establish_connection(self, database_url: str | None = None):
        database_url = (
            database_url or self.database_url or getenv("POSTGRESQL_URL")
        )

        if not database_url:
            raise ValueError(
                "A variável POSTGRESQL_URL não foi encontrada no .env"
            )

        engine_options = {"pool_pre_ping": True}
        if database_url.startswith("sqlite"):
            engine_options["connect_args"] = {"check_same_thread": False}
            if database_url.endswith(":memory:"):
                engine_options["poolclass"] = StaticPool

        self.engine = create_engine(database_url, **engine_options)

        if database_url.startswith("sqlite"):
            @listens_for(self.engine, "connect")
            def enable_sqlite_foreign_keys(connection, _record):
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    def generate_database_schema(self):
        from Infraestrcuture.databases import projeto_model
        from Infraestrcuture.databases import tarefa_model
        from Infraestrcuture.databases import usuario_model

        if self.engine is None:
            raise RuntimeError("A conexão com o banco ainda não foi criada.")
        self.base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        if self.session_factory is None:
            raise RuntimeError("A fábrica de sessões ainda não foi configurada.")
        return self.session_factory()

    def configure_session_factory(self):
        if self.engine is None:
            raise RuntimeError("A conexão com o banco ainda não foi criada.")
        self.session_factory = sessionmaker(bind=self.engine)