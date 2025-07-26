from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class NotionEvent(Base):
	__tablename__ = events
	id = Column(String, primary_key=True)
	event_type = Column(Strin, nullable=False)
	last_edited_time = Column(DateTime)
	payload = Column(String)
	created_at = Column(DateTime, default=datetime.utcnow)