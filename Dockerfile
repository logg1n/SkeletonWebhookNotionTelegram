# Используем python как базу
FROM python:3.11-slim

# Установка зависимостей
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Экспонируем порт, который будет слушать aiohttp
EXPOSE 8080

# Стартовый скрипт (Telegram bot с webhook + очередь + Flask отдельно)
CMD ["python", "start.py"]
