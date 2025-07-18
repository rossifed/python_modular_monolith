from typing import Protocol, runtime_checkable, TypeVar, Generic
from shared.messaging.abstractions import Message

# Définition générique d'un type de evente
E = TypeVar("E", bound="Event")


# Marker Protocol (ne contient rien, juste pour typer les eventes)
@runtime_checkable
class Event(Message, Protocol):
    pass


@runtime_checkable
class EventHandler(Protocol, Generic[E]):
    async def handle(self, event: E) -> None:
        ...


@runtime_checkable
class EventDispatcher(Protocol):
    async def dispatch(self, event: Event) -> None:
        ...
