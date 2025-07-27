import asyncio
import aiohttp
import os
import logging
from importlib.metadata import version
from utils.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Версия SDK
SDK_VERSION = version("notion-client")

async def validate_via_http(token: str, page_id: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    results = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        # /users/me
        try:
            resp = await session.get("https://api.notion.com/v1/users/me")
            results["/users/me"] = (
                "✅ Токен валиден"
                if resp.status == 200
                else f"❌ Ошибка {resp.status}"
            )
        except Exception as e:
            results["/users/me"] = f"❌ Request error: {e}"

        # /pages/{id}
        try:
            url = f"https://api.notion.com/v1/pages/{page_id}"
            resp = await session.get(url)
            if resp.status == 200:
                results["/pages"] = "✅ Доступ к странице есть"
            else:
                results["/pages"] = f"❌ Статус {resp.status}"
        except Exception as e:
            results["/pages"] = f"❌ Request error: {e}"

    return results

async def main():
    token   = settings.notion_token
    page_id = settings.notion_database_id

    logger.info("🔍 Notion Diagnostics")
    logger.info(f"SDK version: {SDK_VERSION}")
    logger.info(f"Token prefix: {token[:5]}…, length={len(token)}")
    logger.info(f"Database/Page ID: {page_id}")

    # HTTP проверка
    results = await validate_via_http(token, page_id)
    for endpoint, status in results.items():
        logger.info(f"{endpoint}: {status}")

if __name__ == "__main__":
    asyncio.run(main())
