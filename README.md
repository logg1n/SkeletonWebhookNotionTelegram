.
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── … ревизии миграций …
│   └── README
│
├── database/
│   ├── __init__.py
│   ├── model.py
│   └── db.py
│
├── notion/
│   ├── notion_diagnostic.py
│   ├── notion_handler.py
│   └── notion_event_storage.py
│
├── telegram_bot/
│   ├── __init__.py
│   ├── bot.py
│   └── routers.py
│
├── server/
│   ├── __init__.py
│   ├── flask.py
│   └── routers.py
│
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── queue.py
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
