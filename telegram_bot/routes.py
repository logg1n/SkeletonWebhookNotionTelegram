# telegram_bot/router.py

from aiogram import Router, types
from aiogram.filters import Command
from utils.queue import notion_queue    # <-- так

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Привет! Я готов принимать задачи из Notion.")

@router.message(Command("ping"))
async def ping_handler(message: types.Message):
    await message.answer("✅ Бот активен и работает.")

@router.message(Command("queue"))
async def queue_size_handler(message: types.Message):
    size = notion_queue.qsize()
    await message.answer(f"📦 В очереди задач: {size}")
