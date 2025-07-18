import importlib
import inspect
import pkgutil
from fastapi import FastAPI
from shared.di.abstractions import DIContainer
from shared.routers.router_registrar import RouterRegistrar
from shared.registrars.config import register_components
from shared.modules.abstractions import Module, ModuleRegistry
from shared.logging.abstractions import Logger
from shared.modules.handler_registration import HandlerRegistration


def load_modules(app: FastAPI,
                 container: DIContainer,
                 logger: Logger,
                 module_base_path="modules"):
    """Charge dynamiquement tous les modules"""

    base_pkg = importlib.import_module(module_base_path)
    registry: ModuleRegistry = container.resolve(ModuleRegistry)
    handler_registration = HandlerRegistration(container, registry)
    for _, module_name, is_pkg in pkgutil.iter_modules(
        base_pkg.__path__,
        prefix=f"{module_base_path}.",
    ):
        if not is_pkg:
            continue

        try:
            # Import du module
            module = importlib.import_module(f"{module_name}.module")

            # Recherche de la classe Module
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if isinstance(cls, type) and cls.__name__.endswith("Module"):
                    module_instance = cls()

                    # Vérification du protocole
                    if not isinstance(module_instance, Module):
                        continue

                    # Vérification si le module est activé
                    if not module_instance.enabled:
                        logger.info(
                            f"⏸️ Module {module_instance.name} disabled"
                            )
                        break

                    logger.info(f"✅ Loading module {module_instance.name}")

                    # Enregistrement des dépendances
                    module_instance.register(container, handler_registration)
                    # register_module_routers(app,
                    #                         module_instance.name,
                    #                         module_base_path)
                    registrars = [
                        RouterRegistrar(app, logger)
                        # CommandHandlerRegistrar(container, logger),
                        # QueryHandlerRegistrar(container, logger),
                        # EventHandlerRegistrar(container, logger)
                    ]

                    register_components(registrars,
                                        module_instance.name,
                                        module_base_path,
                                        logger
                                        )
                    # Initialisation synchrone seulement
                    module_instance.boot(app)

                    break  # On a trouvé et traité le module

        except Exception as e:
            logger.error(f"❌ Failed to load module {module_name}: {e}", True)
