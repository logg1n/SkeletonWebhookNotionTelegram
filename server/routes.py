# routes.py
import logging
import asyncio

from flask import Blueprint, request, jsonify
from utils.queue import notion_queue
from utils.notion_handler import process_notion_event
from utils.config import SERVER_URL
from dotenv import get_key, set_key

logger = logging.getLogger(__name__)

webhook_routes = Blueprint("notion-webhook", __name__)

@notion_routes.route("/notion-webhook", methods=["GET", "POST"])
def notion_webhook():
    try:
        if request.method == "GET":
            return jsonify({"status": "active"}), 200

        data = request.get_json()

        # 👉 Верификация по токену
        token = data.get("verification_token")
        if token:
            logger.info(f"📬 Получен verification_token: {token[:8]}...")
            if not get_key(".env", "NOTION_WEBHOOK_TOKEN"):
                set_key(".env", "NOTION_WEBHOOK_TOKEN", token)
            return jsonify({"challenge": token}), 200

        # 👉 Верификация по challenge
        if data.get("type") == "webhook_verification":
            return jsonify({"challenge": data.get("challenge")}), 200

        # 👉 Обработка основного события
        process_notion_event(data)
        return jsonify({"status": "received"}), 200

    except Exception as e:
        logger.exception("🚨 Ошибка обработки Notion webhook")
        return jsonify({"error": str(e)}), 500
