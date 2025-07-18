import asyncio
from shared.messaging.abstractions import (
    Message,
    MessageBroker,
    MessageChannel,
    AsyncMessageDispatcher,
)


class InMemoryMessageChannel(MessageChannel):
    def __init__(self, max_queue_size: int = 1000):
        self._queue = asyncio.Queue(maxsize=max_queue_size)

    @property
    def writer(self) -> asyncio.Queue:
        return self._queue

    @property
    def reader(self) -> asyncio.Queue:
        return self._queue


class InMemoryMessageBroker(MessageBroker):
    def __init__(self, dispatcher: AsyncMessageDispatcher):
        self._dispatcher = dispatcher

    async def publish_async(self, *messages: Message) -> None:
        valid_messages = [m for m in messages if m is not None]
        tasks = [self._dispatcher.publish_async(m) for m in valid_messages]
        await asyncio.gather(*tasks)
