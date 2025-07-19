from shared.di.abstractions import T, Scope
from typing import Dict, Any
from typing import Type
from shared.di.abstractions import DIContainer


class ServiceScope(Scope):
    def __init__(self, container: DIContainer):  # ← Ajouter container
        self._instances: Dict[Type, Any] = {}
        self._container = container  # ← Stocker le container

    def get_or_create(self, service_type: Type[T], factory: Any) -> T:
        if service_type not in self._instances:
            if callable(factory) and not isinstance(factory, type):
                # ← Passer le container à la factory
                self._instances[service_type] = factory(self._container)
            else:
                self._instances[service_type] = factory()
        return self._instances[service_type]
