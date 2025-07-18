import inspect
from typing import List, Any
from shared.di.abstractions import DIContainer
from shared.events.abstractions import EventHandler
from shared.registrars.abstractions import ComponentRegistrar
from shared.logging.abstractions import Logger


class EventHandlerRegistrar(ComponentRegistrar):
    """Registrar for event handlers"""

    def __init__(self, container: DIContainer, logger: Logger):
        self.container = container
        self.logger = logger

    def is_valid_component(self, obj: Any) -> bool:
        """Check if object is a valid event handler"""
        return (inspect.isclass(obj) and
                issubclass(obj, EventHandler) and
                obj is not EventHandler)

    def register_component(self, component: type, module_name: str,
                           **kwargs) -> None:
        """Register event handler in DI container"""
        event_type = self._get_event_type(component)
        if event_type:
            self.container.add_scoped(event_type, component)
            self.logger.info(f"🎯 Registered {component.__name__} "
                             f"for {event_type.__name__}")

    def get_search_paths(self, module_name: str,
                         module_base_path: str) -> List[str]:
        """Get possible paths for event handlers"""
        return [
            f"{module_base_path}.{module_name}.application",
            f"{module_base_path}.{module_name}.application.handlers",
            f"{module_base_path}.{module_name}.application.events",
            f"{module_base_path}.{module_name}.application.events.handlers",
            f"{module_base_path}.{module_name}.handlers",
            f"{module_base_path}.{module_name}"
        ]

    def should_search_module(self, module_name: str) -> bool:
        """Check if module name suggests it contains handlers"""
        last_part = module_name.split('.')[-1].lower()
        return any(keyword in last_part for keyword in [
            'handler', 'handlers', 'eventhandler', 'eventhandlers'
        ])

    def _get_event_type(self, handler_class: type) -> type | None:
        """Extract event type from handler"""
        try:
            sig = inspect.signature(handler_class.handle)
            params = list(sig.parameters.values())

            if len(params) >= 2:  # self + event
                event_type = params[1].annotation
                if (event_type != inspect.Parameter.empty and
                        inspect.isclass(event_type)):
                    return event_type
        except Exception:
            pass
        return None
