
import inspect
from shared.modules.module_registry import DefaultModuleRegistry
from shared.modules.module_client import DefaultModuleClient
from shared.di.abstractions import DIContainer
from shared.modules.abstractions import ModuleRegistry, ModuleClient


def register_handlers(registry: ModuleRegistry, module):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj, "handle"):
            # Suppose que l'argument du handle donne le type du message
            sig = inspect.signature(obj.handle)
            message_type = list(sig.parameters.values())[1].annotation
            registry.add_broadcast_handler(message_type, obj().handle)


def configure_modules(container: DIContainer):
    container.add_singleton(ModuleRegistry, DefaultModuleRegistry)
    container.add_singleton(ModuleClient,
                            lambda: DefaultModuleClient(
                                container.resolve(ModuleRegistry)),)
