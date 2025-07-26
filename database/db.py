from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 🔧 путь к SQLite-файлу, можно заменить на PostgreSQL URI
DATABASE_URL = "sqlite:///notion_events.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
