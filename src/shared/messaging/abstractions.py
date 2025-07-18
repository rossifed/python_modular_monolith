from typing import Protocol, runtime_checkable
from asyncio import Queue


@runtime_checkable
class Message(Protocol):
    ...


@runtime_checkable
class MessageBroker(Protocol):
    async def publish_async(self, *messages: Message) -> None:
        ...


class MessageEnvelope:
    def __init__(self, message: Message):
        self.message = message


@runtime_checkable
class MessageChannel(Protocol):
    @property
    def writer(self) -> Queue[MessageEnvelope]:
        ...

    @property
    def reader(self) -> Queue[MessageEnvelope]:
        ...


@runtime_checkable
class AsyncMessageDispatcher(Protocol):
    async def publish_async(self, message: Message) -> None:
        ...


@runtime_checkable
class ModuleClient(Protocol):
    async def publish_async(self, message: Message) -> None:
        ...
