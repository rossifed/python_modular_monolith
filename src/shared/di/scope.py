from shared.di.abstractions import T, Scope
from typing import Dict, Any
from typing import Type


class ServiceScope(Scope):
    """Contexte pour gérer les instances scoped d'une requête"""
    def __init__(self):
        self._instances: Dict[Type, Any] = {}

    def get_or_create(self, service_type: Type[T], factory: Type[T]) -> T:
        if service_type not in self._instances:
            self._instances[service_type] = factory()
        return self._instances[service_type]

    def clear(self):
        self._instances.clear()
