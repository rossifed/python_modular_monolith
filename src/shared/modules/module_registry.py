
from collections import defaultdict
from typing import Callable, Type, Dict, List
from shared.modules.abstractions import ModuleRegistry


class DefaultModuleRegistry(ModuleRegistry):
    def __init__(self):
        self._broadcast_handlers: Dict[
            Type,
            List[Callable]
            ] = defaultdict(list)

    def add_broadcast_handler(self, message_type: Type, handler: Callable):
        self._broadcast_handlers[message_type].append(handler)

    def get_broadcast_handlers(self, message_type: Type):
        return self._broadcast_handlers.get(message_type, [])
