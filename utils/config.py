# utils/config.py

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # 1. Окружение
    ENV: str = Field("development", env="ENV")
    DEBUG: bool = Field(True, env="DEBUG")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    # 2. База данных
    DATABASE_URL: str = Field(
        "sqlite:///./app.db",
        env="DATABASE_URL",
        description="sqlite:///./app.db или postgresql://user:pass@host/dbname"
    )

    # 3. Telegram
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    CHAT_ID: int = Field(..., env="CHAT_ID")

    # 4. Webhook (Telegram)
    SERVER_URL: HttpUrl = Field(..., env="SERVER_URL")
    WEBHOOK_PATH: str = Field("/telegram-webhook", env="WEBHOOK_PATH")

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.SERVER_URL.rstrip('/')}{self.WEBHOOK_PATH}"

    # 5. Notion
    NOTION_TOKEN: str = Field(..., env="NOTION_TOKEN")
    NOTION_DATABASE_ID: str = Field(..., env="NOTION_DATABASE_ID")
    NOTION_WEBHOOK_TOKEN: str = Field("", env="NOTION_WEBHOOK_TOKEN")
    NOTION_QUEUE_MAXSIZE: int = Field(100, env="NOTION_QUEUE_MAXSIZE")

    # 6. Celery
    CELERY_BROKER_URL: str = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(..., env="CELERY_RESULT_BACKEND")


# Единственный экземпляр настроек
settings = Settings()
