from typing import Protocol, TypeVar
from shared.commands.abstractions import Command
from shared.events.abstractions import Event
from shared.queries.abstractions import Query

TResult = TypeVar("TResult")


class Dispatcher(Protocol):
    async def send(self, command: Command) -> None:
        ...

    async def publish(self, event: Event) -> None:
        ...

    async def query(self, query: Query[TResult]) -> TResult:
        ...
