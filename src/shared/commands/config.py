from shared.di.abstractions import DIContainer
from shared.commands.abstractions import CommandDispatcher
from shared.commands.command_dispatcher import DefaultCommandDispatcher


def configure_commands(container: DIContainer):
    container.add_singleton(CommandDispatcher,
                            lambda: DefaultCommandDispatcher(container))
