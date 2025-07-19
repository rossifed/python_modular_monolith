from fastapi import FastAPI
from typing import Protocol, runtime_checkable
from shared.di import DIContainer
from typing import Callable, Type, Optional, Any


@runtime_checkable
class HandlerRegistrar(Protocol):
    def register(self, message_type: Type,
                 handler_type: Type,
                 factory: Optional[Callable[[DIContainer], Any]] = None
                 ) -> None:
        ...


@runtime_checkable
class Module(Protocol):
    name: str
    enabled: bool  # indique si le module est actif ou non

    def register_services(self,
                          container: DIContainer) -> None:
        """Registration of module services"""
        ...

    def register_handlers(self,
                          handler_registration: HandlerRegistrar) -> None:
        """Registration of module services"""
        ...

    def boot(self, app: FastAPI) -> None:
        """Synchonous initilaization"""
        ...


class ModuleRegistry(Protocol):

    def add_broadcast_handler(self, key: str, handler: Callable):
        ...

    def get_broadcast_handlers(self, key: str):
        ...


class ModuleClient(Protocol):

    async def publish_async(self, message):
        ...
