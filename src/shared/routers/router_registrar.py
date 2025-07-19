import importlib
from typing import List, Any, Optional
from fastapi import APIRouter, FastAPI
from shared.logging import Logger


class RouterRegistrar:
    """Registrar for FastAPI routers"""

    def __init__(self, app: FastAPI, logger: Logger):
        self.app = app
        self.logger = logger

    def is_valid_component(self, obj: Any) -> bool:
        """Check if object is a valid router"""
        return isinstance(obj, APIRouter) and obj.routes

    def register_component(self, component: APIRouter,
                           module_name: str, **kwargs) -> None:
        """Register router in FastAPI app"""
        # Default configuration
        prefix = f"/api/{module_name.replace('_', '-')}"
        tags = [module_name.replace("_", " ").title()]

        # Look for custom configuration
        config = self._get_router_config(component)
        if config:
            prefix = config.get("prefix", prefix)
            tags = config.get("tags", tags)

        # Register the router
        self.app.include_router(component, prefix=prefix, tags=tags)
        self.logger.info(f"📍 Registered router for module"
                         f"'{module_name}' at {prefix}")

    def get_search_paths(self, module_name: str,
                         module_base_path: str) -> List[str]:
        """Get possible paths for API routers"""
        return [
            f"{module_base_path}.{module_name}.api",
            f"{module_base_path}.{module_name}.api.routers",
            f"{module_base_path}.{module_name}.routers",
            f"{module_base_path}.{module_name}"
        ]

    def should_search_module(self, module_name: str) -> bool:
        """Always search all modules for routers"""
        return True

    def _get_router_config(self, router: APIRouter) -> Optional[dict]:
        """Get router configuration"""
        # 1. Config on the router itself
        if hasattr(router, 'config'):
            return router.config

        # 2. Config in the module
        try:
            if router.routes:
                first_route = next(iter(router.routes))
                if hasattr(first_route, 'endpoint'):
                    endpoint_module = importlib.import_module(
                        first_route.endpoint.__module__
                        )
                    if hasattr(endpoint_module, 'MODULE_CONFIG'):
                        return endpoint_module.MODULE_CONFIG
        except (ImportError, AttributeError, StopIteration, TypeError):
            pass

        return None
