from typing import Protocol, runtime_checkable, TypeVar, Generic
from shared.messaging import Message

R = TypeVar("Result")
Q = TypeVar("Q", bound="Query[R]")


# Marker Protocol (ne contient rien, juste pour typer les queryes)
@runtime_checkable
class Query(Protocol, Generic[R]):
    pass


@runtime_checkable
class QueryHandler(Message, Protocol, Generic[Q, R]):
    async def handle(self, query: Q) -> R:
        ...


@runtime_checkable
class QueryDispatcher(Protocol):
    async def dispatch(self, query: Query[R]) -> R:
        ...
