

from shared.di import DIContainer
from shared.events import EventDispatcher
from shared.events import DefaultEventDispatcher


def configure_events(container: DIContainer):
    container.add_singleton(EventDispatcher,
                            lambda: DefaultEventDispatcher(container))
