from sqlalchemy.orm import Session
from database import NotionEvent

def is_duplicate_event(db: Session, entity_id: str, last_edited_time: str) -> bool:
    """
    Возвращает True, если событие с таким ID и временем уже есть в БД.
    """
    return (
        db.query(NotionEvent)
          .filter_by(id=entity_id, last_edited_time=last_edited_time)
          .first()
        is not None
    )

def save_notion_event(db: Session, raw: dict) -> None:
    """
    Сохраняет сырое событие Notion в таблицу NotionEvent.
    """
    entity   = raw.get("entity", {})
    data     = raw.get("data", {})
    event = NotionEvent(
        id               = entity.get("id"),
        event_type       = raw.get("type"),
        last_edited_time = data.get("last_edited_time"),
        payload          = json.dumps(raw, ensure_ascii=False)
    )
    db.add(event)
    db.commit()
