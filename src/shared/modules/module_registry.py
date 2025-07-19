
from collections import defaultdict
from typing import Callable, Type, Dict, List
from shared.modules import ModuleRegistry


class DefaultModuleRegistry(ModuleRegistry):
    def __init__(self):
        self._broadcast_handlers: Dict[
            Type,
            List[Callable]
            ] = defaultdict(list)

    def add_broadcast_handler(self, key: str, handler: Callable):
        self._broadcast_handlers[key].append(handler)

    def get_broadcast_handlers(self, key: str):
        return self._broadcast_handlers.get(key, [])
