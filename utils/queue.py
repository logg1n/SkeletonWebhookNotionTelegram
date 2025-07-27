# utils/queue.py

from queue import Queue
from utils.config import settings

# обращаемся к существующему атрибуту
notion_queue: Queue = Queue(maxsize=settings.NOTION_QUEUE_MAXSIZE)
