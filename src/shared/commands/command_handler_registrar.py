import inspect
from typing import List, Any
from shared.di import DIContainer
from shared.commands import CommandHandler
from shared.registrars.abstractions import ComponentRegistrar
from shared.logging import Logger


class CommandHandlerRegistrar(ComponentRegistrar):
    """Registrar for command handlers"""

    def __init__(self, container: DIContainer, logger: Logger):
        self.container = container
        self.logger = logger

    def is_valid_component(self, obj: Any) -> bool:
        """Check if object is a valid command handler"""
        return (inspect.isclass(obj) and
                issubclass(obj, CommandHandler) and
                obj is not CommandHandler)

    def register_component(self, component: type, module_name: str,
                           **kwargs) -> None:
        """Register command handler in DI container"""
        command_type = self._get_command_type(component)
        if command_type:
            self.container.add_scoped(command_type, component)
            self.logger.info(f"🎯 Registered {component.__name__} "
                             f"for {command_type.__name__}")

    def get_search_paths(self, module_name: str,
                         module_base_path: str) -> List[str]:
        """Get possible paths for command handlers"""
        return [
            f"{module_base_path}.{module_name}.application",
            f"{module_base_path}.{module_name}.application.handlers",
            f"{module_base_path}.{module_name}.application.commands",
            f"{module_base_path}.{module_name}.application.commands.handlers",
            f"{module_base_path}.{module_name}.handlers",
            f"{module_base_path}.{module_name}"
        ]

    def should_search_module(self, module_name: str) -> bool:
        """Check if module name suggests it contains handlers"""
        last_part = module_name.split('.')[-1].lower()
        return any(keyword in last_part for keyword in [
            'handler', 'handlers', 'commandhandler', 'commandhandlers'
        ])

    def _get_command_type(self, handler_class: type) -> type | None:
        """Extract command type from handler"""
        try:
            sig = inspect.signature(handler_class.handle)
            params = list(sig.parameters.values())

            if len(params) >= 2:  # self + command
                command_type = params[1].annotation
                if (command_type != inspect.Parameter.empty and
                        inspect.isclass(command_type)):
                    return command_type
        except Exception:
            pass
        return None
