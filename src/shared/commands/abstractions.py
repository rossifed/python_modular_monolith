from typing import Protocol, runtime_checkable, TypeVar, Generic
from shared.messaging.abstractions import Message


# Définition générique d'un type de commande
C = TypeVar("C", bound="Command")


# Marker Protocol (ne contient rien, juste pour typer les commandes)
@runtime_checkable
class Command(Message, Protocol):
    pass


@runtime_checkable
class CommandHandler(Protocol, Generic[C]):
    async def handle(self, command: C) -> None:
        ...


@runtime_checkable
class CommandDispatcher(Protocol):
    async def dispatch(self, command: Command) -> None:
        ...
