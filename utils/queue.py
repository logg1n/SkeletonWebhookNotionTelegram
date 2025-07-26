import asyncio

class NotionQueue:
    _instance = None
    _queue = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotionQueue, cls).__new__(cls)
            cls._queue = asyncio.Queue()
        return cls._instance

    def put(self, item):
        return self._queue.put(item)

    async def get(self):
        return await self._queue.get()

    def qsize(self):
        return self._queue.qsize()

# Глобальный объект для импорта
notion_queue = NotionQueue()
