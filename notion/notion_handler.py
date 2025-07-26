import asyncio
import logging

from utils.queue import notion_queue
from utils.telegram import send_telegram_notification
from utils.utils import format_notion_telegram_message
from utils.cache_store import is_duplicate_event  # предположим, ты добавил это

logger = logging.getLogger(__name__)

VALID_EVENTS = {
	"page.content_updated", "page.created", "page.deleted", "page.locked",
	"page.unlocked", "page.moved", "page.properties_updated", "page.undeleted",
	"database.content_updated", "database.created", "database.deleted",
	"database.moved", "database.schema_updated", "database.undeleted",
	"comment.created", "comment.deleted", "comment.updated"
}


class NotionEventProcessor:

	def is_supported(self, event_type: str) -> bool:
		return event_type in VALID_EVENTS

	def extract_core_fields(self, data: dict) -> dict:
		props = data.get("properties", {})
		title = props.get("Название", {}).get("title", [])
		status = props.get("Статус", {}).get("select", {}).get("name")
		category = props.get("Категория", {}).get("select", {}).get("name")
		number = props.get("Number", {}).get("number")
		subcategory = props.get("Подкатегория", {}).get("multi_select", [])

		return {
			"Название": title[0]["text"]["content"] if title else "—",
			"Категория": category or "—",
			"Статус": status or "—",
			"Number": number or "—",
			"Подкатегория": [tag["name"] for tag in subcategory] if subcategory else "—",
		}

	async def send_to_queue(self, fields: dict):
		message = format_notion_telegram_message([fields])
		await notion_queue.put(message)

	def process(self, raw: dict):
		event_type = raw.get("type")
		entity = raw.get("entity", {})
		data = raw.get("data", {})
		entity_type = entity.get("type")
		entity_id = entity.get("id")
		last_edited_time = data.get("last_edited_time")

		if not self.is_supported(event_type):
			logger.warning(f"⚠️ Неизвестное событие: {event_type}")
			return {"message": "Событие не поддерживается"}

		if is_duplicate_event(entity_id, last_edited_time):
			logger.info(f"⏹️ Повтор события: {entity_id} уже обработан")
			return {"message": "Повторное событие — пропущено"}

		logger.info(f"📌 Событие: {event_type} (entity: {entity_type}, id: {entity_id})")

		fields = self.extract_core_fields(data)
		asyncio.run(self.send_to_queue(fields))

		return {"message": "✅ Обновление отправлено"}
