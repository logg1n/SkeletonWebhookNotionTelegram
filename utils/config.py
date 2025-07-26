import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name: str, default: str = None, required: bool = False):
    value = os.getenv(name, default)
    if required and (value is None or value.strip() == ""):
        raise ValueError(f"⛔ Переменная окружения '{name}' обязательна, но не задана.")
    return value

# 🔐 Telegram
BOT_TOKEN = get_env_var("BOT_TOKEN", required=True)
CHAT_ID = get_env_var("CHAT_ID", required=True)

# 🌐 Webhook
SERVER_URL = get_env_var("SERVER_URL", required=True)
WEBHOOK_PATH = get_env_var("WEBHOOK_PATH", "/telegram-webhook")
WEBHOOK_URL = get_env_var("WEBHOOK_URL", f"{SERVER_URL}{WEBHOOK_PATH}")
SERVER_URL = os.getenv("SERVER_URL")  # например: https://your-domain.up.railway.app


# 🧠 Notion
NOTION_TOKEN = get_env_var("NOTION_TOKEN", required=True)
DATABASE_ID = get_env_var("DATABASE_ID", required=True)
NOTION_WEBHOOK_TOKEN = get_env_var("NOTION_WEBHOOK_TOKEN", default="")
