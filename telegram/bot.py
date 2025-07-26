import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler, setup_application)
from aiohttp import web

from telegram import router
from utils import notion_queue
from utils.config import BOT_TOKEN, WEBHOOK_URL, CHAT_ID, SERVER_URL




WEBHOOK_PATH = "/telegram-webhook"
PORT = 8080  # Порт, на котором будет работать aiohttp-сервер

# 🤖 Инициализация Telegram-бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(router)

# 📦 Обработка очереди
async def process_queue():
    while True:
        try:
            message = await notion_queue.get()
            if message:
                await bot.send_message(chat_id=CHAT_ID, text=message)
            else:
                print("⚠️ Пустое сообщение — пропущено.")
        except Exception as e:
            print(f"🚨 Ошибка отправки: {e}")

# 🌐 Webhook-инициализация
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(process_queue())
    print("🚀 Webhook установлен:", WEBHOOK_URL)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    print("🛑 Webhook удалён")

def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, port=PORT)

if __name__ == "__main__":
    main()
