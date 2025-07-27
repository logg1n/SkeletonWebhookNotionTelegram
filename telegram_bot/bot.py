import asyncio
import logging
from contextlib import suppress

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application

from telegram_bot import router
from utils.config import settings
from utils.queue import notion_queue

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(router)


async def process_queue():
    """Бесконечно обрабатываем очередь и отправляем сообщения в Telegram."""
    logger.info("▶️ Старт обработки очереди")
    while True:
        msg = await notion_queue.get()
        try:
            if msg:
                await bot.send_message(chat_id=settings.chat_id, text=msg)
            else:
                logger.warning("⚠️ Пустое сообщение — пропущено.")
        except Exception:
            logger.exception("🚨 Ошибка при отправке сообщения")
        finally:
            notion_queue.task_done()
        await asyncio.sleep(0.01)


async def on_startup(app: web.Application):
    """Устанавливаем webhook и запускаем обработчик очереди."""
    await bot.set_webhook(settings.webhook_url)
    logger.info(f"🚀 Webhook установлен: {settings.webhook_url}")

    task = asyncio.create_task(process_queue())
    app["queue_task"] = task


async def on_shutdown(app: web.Application):
    """Удаляем webhook и корректно завершаем очередь."""
    logger.info("🛑 Шутдаун: удаляем webhook и отменяем таски")
    with suppress(Exception):
        await bot.delete_webhook()

    task = app.get("queue_task")
    if task:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    with suppress(Exception):
        await bot.session.close()


def create_app() -> web.Application:
    """Фабрика aiohttp-приложения с Aiogram-webhook."""
    app = web.Application()
    setup_application(app, dp, bot=bot, path=settings.webhook_path)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    async def health(request):
        return web.json_response({"status": "ok"})
    app.router.add_get("/health", health)

    return app


def main():
    """Точка входа: создаём приложение и запускаем aiohttp-сервер."""
    app = create_app()
    logger.info(f"📡 Запуск Telegram-бота на порту {settings.port}")
    web.run_app(app, port=settings.port)


if __name__ == "__main__":
    main()
