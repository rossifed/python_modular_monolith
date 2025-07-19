import inspect
from typing import List, Any
from shared.di import DIContainer
from shared.queries import QueryHandler
from shared.registrars.abstractions import ComponentRegistrar
from shared.logging import Logger


class QueryHandlerRegistrar(ComponentRegistrar):
    """Registrar for query handlers"""

    def __init__(self, container: DIContainer, logger: Logger):
        self.container = container
        self.logger = logger

    def is_valid_component(self, obj: Any) -> bool:
        """Check if object is a valid query handler"""
        return (inspect.isclass(obj) and
                issubclass(obj, QueryHandler) and
                obj is not QueryHandler)

    def register_component(self, component: type, module_name: str,
                           **kwargs) -> None:
        """Register query handler in DI container"""
        query_type = self._get_query_type(component)
        self.logger.info(f"Registering {query_type} id= {id(query_type)}")
        if query_type:
            self.container.add_scoped(query_type, component)
            self.logger.info(f"🎯 Registered {component.__name__} "
                             f"for {query_type.__name__}")

    def get_search_paths(self, module_name: str,
                         module_base_path: str) -> List[str]:
        """Get possible paths for query handlers"""
        return [
            f"{module_base_path}.{module_name}.application",
            f"{module_base_path}.{module_name}.application.handlers",
            f"{module_base_path}.{module_name}.application.queries",
            f"{module_base_path}.{module_name}.application.queries.handlers",
            f"{module_base_path}.{module_name}.handlers",
            f"{module_base_path}.{module_name}"
        ]

    def should_search_module(self, module_name: str) -> bool:
        """Check if module name suggests it contains handlers"""
        last_part = module_name.split('.')[-1].lower()
        return any(keyword in last_part for keyword in [
            'handler', 'handlers', 'queryhandler', 'queryhandlers'
        ])

    def _get_query_type(self, handler_class: type) -> type | None:
        """Extract query type from handler"""
        try:
            sig = inspect.signature(handler_class.handle)
            params = list(sig.parameters.values())

            if len(params) >= 2:  # self + query
                query_type = params[1].annotation
                if (query_type != inspect.Parameter.empty and
                        inspect.isclass(query_type)):
                    return query_type
        except Exception:
            pass
        return None
