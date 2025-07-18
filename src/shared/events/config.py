

from shared.di.abstractions import DIContainer
from shared.events.abstractions import EventDispatcher
from shared.events.default_event_dispatcher import DefaultEventDispatcher


def configure_events(container: DIContainer):
    container.add_singleton(EventDispatcher,
                            lambda: DefaultEventDispatcher(container))
