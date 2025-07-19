import importlib
import pkgutil
import inspect
from typing import List, Any
from shared.registrars.abstractions import ComponentRegistrar
from shared.logging import Logger


def register_components(
    registrars: List[ComponentRegistrar],
    module_name: str,
    module_base_path: str,
    logger: Logger,
    **kwargs
) -> None:
    """Discover and register all components for all registrars"""
    for registrar in registrars:
        _discover_for_registrar(registrar,
                                module_name,
                                module_base_path,
                                logger=logger,
                                **kwargs)


def _discover_for_registrar(registrar: ComponentRegistrar,
                            module_name: str,
                            module_base_path: str,
                            logger: Logger = None,
                            **kwargs) -> None:
    """Discover components for a specific registrar"""
    search_paths = registrar.get_search_paths(module_name, module_base_path)
    seen_components = set()
    total_components = 0

    for search_path in search_paths:
        components = _discover_in_path(search_path, registrar, logger=logger)

        for component in components:
            if id(component) in seen_components:
                continue

            seen_components.add(id(component))
            registrar.register_component(component,
                                         module_name=module_name, **kwargs)
            total_components += 1

    if total_components == 0 and logger:
        component_type = registrar.__class__.__name__.replace('Registrar', '')
        logger.info(f"📭 No {component_type} found for module '{module_name}'")


def _discover_in_path(module_path: str,
                      registrar: ComponentRegistrar,
                      logger: Logger = None
                      ) -> List[Any]:
    """Discover components in a specific module path"""
    components = []

    try:
        main_module = importlib.import_module(module_path)
        components.extend(_find_in_module(main_module, registrar))

        if hasattr(main_module, '__path__'):
            for _, sub_module_name, _ in pkgutil.iter_modules(
                main_module.__path__,
                prefix=f"{module_path}."
            ):
                try:
                    if registrar.should_search_module(sub_module_name):
                        sub_module = importlib.import_module(sub_module_name)
                        components.extend(
                            _find_in_module(sub_module, registrar)
                            )
                except Exception as e:
                    if logger:
                        logger.warning(
                            f"⚠️ Could not import {sub_module_name}: {e}"
                            )

    except ImportError:
        # Normal: module might not exist
        pass
    except Exception as e:
        if logger:
            logger.error(f"❌ Error discovering in {module_path}: {e}")

    return components


def _find_in_module(module: Any, registrar: ComponentRegistrar) -> List[Any]:
    """Find components in a given module"""
    components = []

    for name, obj in inspect.getmembers(module):
        if registrar.is_valid_component(obj):
            components.append(obj)

    return components
