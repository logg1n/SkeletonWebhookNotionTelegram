from database import NotionEvent
from sqlalchemy.orm import Session


def is_duplicate_event(db: Session, entity_id: str, last_edited_time: str) -> bool:
	return db.query(NotionEvent).filter_by(id=entity_id, last_edited_time=last_edited_time).first() is not None


def save_notion_event(db: Session, raw: dict):
	entity = raw.get("entity", {})
	data = raw.get("data", {})

	event = NotionEvent(
		id=entity.get("id"),
		event_type=raw.get("type"),
		last_edited_time=data.get("last_edited_time"),
		payload=str(raw),  # можно использовать json.dumps(raw) если хочешь сериализовать красиво
	)
	db.add(event)
	db.commit()
