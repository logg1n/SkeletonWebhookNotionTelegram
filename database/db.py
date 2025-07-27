# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import settings
from database import Base

# Для SQLite: отключаем проверку одного потока
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)

# Генератор сессий
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def init_db() -> None:
    """
    Создаёт все таблицы в базе данных.
    Вызывать при старте приложения.
    """
    Base.metadata.create_all(bind=engine)
