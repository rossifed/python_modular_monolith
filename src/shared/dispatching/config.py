# shared/dispatching/config.py

from shared.di.abstractions import DIContainer
from shared.dispatching.default_dispatcher import DefaultDispatcher
from shared.dispatching.abstractions import Dispatcher
from shared.commands.abstractions import CommandDispatcher
from shared.queries.abstractions import QueryDispatcher
from shared.events.abstractions import EventDispatcher


def configure_dispatching(container: DIContainer) -> None:
    """Register the unified Dispatcher in the DI container."""
    container.add_singleton(Dispatcher, lambda: DefaultDispatcher(
        command_dispatcher=container.resolve(CommandDispatcher),
        event_dispatcher=container.resolve(EventDispatcher),
        query_dispatcher=container.resolve(QueryDispatcher),
    ))
