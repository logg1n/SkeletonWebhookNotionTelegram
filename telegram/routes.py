from aiogram import Router, types
from aiogram.filters import Command

from utils import notion_queue

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
    await message.answer(f"📦 Количество задач в очереди: {size}")
