# model.py

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class NotionEvent(Base):
    __tablename__ = "notion_events"

    # Уникальный UUID или другой строковый идентификатор события
    id = Column(String, primary_key=True, index=True)

    # Тип события (создание, обновление и т. д.)
    event_type = Column(String, nullable=False)

    # Время последнего изменения в Notion
    last_edited_time = Column(DateTime, nullable=True)

    # Полная полезная нагрузка события (JSON-строка)
    payload = Column(Text, nullable=True)

    # Время сохранения в локальную БД
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
