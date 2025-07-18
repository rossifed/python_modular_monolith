from fastapi import FastAPI
from typing import Protocol, runtime_checkable
from shared.di.abstractions import DIContainer
from typing import Callable, Type


@runtime_checkable
class HandlerRegistrar(Protocol):
    def register(self, message_type: Type,
                 handler_type: Type,
                 factory: Callable[[], any] = ...) -> None:
        ...


@runtime_checkable
class Module(Protocol):
    name: str
    enabled: bool  # indique si le module est actif ou non

    def register(self, container: DIContainer,
                 handler_registration: HandlerRegistrar) -> None:
        """Registration of module services"""
        ...

    def boot(self, app: FastAPI) -> None:
        """Synchonous initilaization"""
        ...


class ModuleRegistry(Protocol):

    def add_broadcast_handler(self, message_type: Type, handler: Callable):
        ...

    def get_broadcast_handlers(self, message_type: Type):
        ...


class ModuleClient(Protocol):

    async def publish_async(self, message):
        ...
