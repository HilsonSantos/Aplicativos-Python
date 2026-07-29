"""Configuração de conexão e sessão do banco de dados."""

import os
from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("APPVET_DATABASE_URL", "sqlite:///./appvet.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
        """Mantém a integridade referencial, desativada por padrão no SQLite."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Classe base declarativa para todos os modelos ORM."""


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessão de banco de dados por requisição (dependency do FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria todas as tabelas no banco de dados, caso não existam."""
    from appvet import models  # noqa: F401  (garante que os modelos sejam registrados)

    Base.metadata.create_all(bind=engine)
