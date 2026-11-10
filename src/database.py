import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from src.models import Base
except ImportError:  # pragma: no cover
    from models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "roupas_loja.db"


def get_mysql_url() -> str | None:
    host = os.getenv("MYSQL_HOST")
    if not host:
        return None

    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "roupas_loja")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")
    if database_url:
        return database_url

    if os.getenv("APP_ENV", "local").lower() == "production" or os.getenv("MYSQL_HOST"):
        mysql_url = get_mysql_url()
        if mysql_url:
            return mysql_url

    return f"sqlite:///{DB_PATH}"


engine = create_engine(get_database_url(), echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
