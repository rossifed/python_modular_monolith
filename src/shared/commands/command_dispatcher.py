from shared.di import DIContainer
from shared.commands import Command, CommandDispatcher


class DefaultCommandDispatcher(CommandDispatcher):
    """Simple command dispatcher using DI container"""

    def __init__(self, container: DIContainer):
        self.container = container

    async def dispatch(self, command: Command) -> None:
        """Dispatch a command to its handler"""
        command_type = type(command)

        # Resolve handler directly by command type from DI container
        handler = self.container.resolve(command_type)
        await handler.handle(command)
