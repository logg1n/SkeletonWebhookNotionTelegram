# server.py
import logging
from flask import Blueprint, request, jsonify
from dotenv import get_key, set_key

from notion import process_notion_event
from utils import settings

logger = logging.getLogger(__name__)
webhook_routes = Blueprint("notion-webhook", __name__)


@webhook_routes.route(settings.webhook_path, methods=["GET", "POST"])
def notion_webhook():
    try:
        # Health‐check
        if request.method == "GET":
            return jsonify({"status": "ok"}), 200

        payload = request.get_json(force=True)

        # 1️⃣ Пишем verification_token в .env при первой настройке
        token = payload.get("verification_token")
        if token:
            logger.info(f"Got verification token: {token[:8]}…")
            if not get_key(settings.Config.env_file, "NOTION_WEBHOOK_TOKEN"):
                set_key(settings.Config.env_file, "NOTION_WEBHOOK_TOKEN", token)
            return jsonify({"challenge": token}), 200

        # 2️⃣ Challenge‐verification от Notion
        if payload.get("type") == "webhook_verification":
            return jsonify({"challenge": payload["challenge"]}), 200

        # 3️⃣ Обработка бизнес‐логики
        process_notion_event(payload)
        return jsonify({"status": "received"}), 200

    except Exception as e:
        logger.exception("Error handling Notion webhook")
        return jsonify({"error": str(e)}), 500
