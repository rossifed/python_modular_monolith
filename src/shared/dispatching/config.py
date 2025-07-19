# shared/dispatching/config.py

from shared.di import DIContainer
from shared.dispatching import DefaultDispatcher, Dispatcher
from shared.commands import CommandDispatcher
from shared.queries import QueryDispatcher
from shared.events import EventDispatcher


def configure_dispatching(container: DIContainer) -> None:
    """Register the unified Dispatcher in the DI container."""
    container.add_singleton(Dispatcher, lambda: DefaultDispatcher(
        command_dispatcher=container.resolve(CommandDispatcher),
        event_dispatcher=container.resolve(EventDispatcher),
        query_dispatcher=container.resolve(QueryDispatcher),
    ))
