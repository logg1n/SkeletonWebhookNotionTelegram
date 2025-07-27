import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ─── Добавляем корень проекта в sys.path ────────────────────────────────────
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# ─── Импорты ваших настроек и моделей ──────────────────────────────────────
from utils.config import settings          # Pydantic-настройки с DATABASE_URL
from database.model import Base           # Base ваших моделей

# ─── Настройка Alembic ────────────────────────────────────────────────────
config = context.config
fileConfig(config.config_file_name)

# Подменяем URL-строку на ту, что в .env через Pydantic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Метаданные таблиц для автогенерации
target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в offline режиме (генерация SQL скриптов)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в online режиме (прямое соединение)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# Выбор режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
