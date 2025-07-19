from shared.di.abstractions import DIContainer
from shared.modules.abstractions import ModuleRegistry, HandlerRegistrar
from typing import Type, Callable, Any, Optional


class HandlerRegistration(HandlerRegistrar):
    def __init__(self, container: DIContainer, registry: ModuleRegistry):
        self._container = container
        self._registry = registry

    def register(self, message_type: Type,
                 handler_type: Type,
                 factory: Optional[Callable[[DIContainer], Any]] = None
                 ) -> None:
        # 1. Enregistrement dans le container avec factory si fournie
        if factory is not None:
            self._container.add_scoped(message_type,
                                       factory(self._container))
        else:
            self._container.add_scoped(message_type, handler_type)

        # 2. Création du handler à l'exécution pour chaque message
        async def handler_function(message):
            instance = self._container.resolve(message_type)
            return await instance.handle(message)

        self._registry.add_broadcast_handler(message_type.__name__,
                                             handler_function)
