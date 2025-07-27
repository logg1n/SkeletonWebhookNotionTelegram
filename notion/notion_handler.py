import logging

from sqlalchemy.orm import Session
from utils.queue import notion_queue
from utils.utils import format_notion_telegram_message
from .notion_event_storage import is_duplicate_event, save_notion_event

logger = logging.getLogger(__name__)

# Список поддерживаемых типов событий
VALID_EVENTS = {
	"page.content_updated", "page.created", "page.deleted", "page.locked",
	"page.unlocked", "page.moved", "page.properties_updated", "page.undeleted",
	"database.content_updated", "database.created", "database.deleted",
	"database.moved", "database.schema_updated", "database.undeleted",
	"comment.created", "comment.deleted", "comment.updated"
}


class NotionEventProcessor:
    async def process(
        self,
        raw: dict,
        db: Session
    ) -> dict[str, str]:
        """
        Обрабатывает одно webhook-событие Notion:
        - проверяет тип
        - проверяет дубликаты
        - сохраняет в БД
        - кладёт сообщение в очередь
        """
        event_type = raw.get("type")
        entity     = raw.get("entity", {})
        data       = raw.get("data", {})

        entity_id        = entity.get("id")
        last_edited_time = data.get("last_edited_time")

        if event_type not in VALID_EVENTS:
            logger.warning(f"⚠️ Неподдерживаемый тип: {event_type}")
            return {"message": "Event not supported"}

        if is_duplicate_event(db, entity_id, last_edited_time):
            logger.info(f"⏹️ Дубликат: {entity_id}")
            return {"message": "Duplicate — skipped"}

        # Сохраняем в БД
        save_notion_event(db, raw)

        # Формируем и отправляем в очередь
        props  = self._extract_core_fields(data)
        text   = format_notion_telegram_message([props])
        await notion_queue.put(text)

        logger.info(f"✅ Отправлено в очередь: {entity_id}")
        return {"message": "Delivered to queue"}

    def _extract_core_fields(self, data: dict) -> dict:
        props = data.get("properties", {})
        # Пример извлечения полей
        title = props.get("Название", {}).get("title", [])
        return {
            "Название": title[0]["text"]["content"] if title else "—",
            # остальные поля…
        }
