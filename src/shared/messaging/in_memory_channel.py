import asyncio
from shared.messaging import (
    MessageChannel)


class InMemoryMessageChannel(MessageChannel):
    def __init__(self, max_queue_size: int = 1000):
        self._queue = asyncio.Queue(maxsize=max_queue_size)

    @property
    def writer(self) -> asyncio.Queue:
        return self._queue

    @property
    def reader(self) -> asyncio.Queue:
        return self._queue
