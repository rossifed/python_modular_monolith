from shared.di import DIContainer
from shared.commands import CommandDispatcher
from shared.commands import DefaultCommandDispatcher


def configure_commands(container: DIContainer):
    container.add_singleton(CommandDispatcher,
                            lambda: DefaultCommandDispatcher(container))
