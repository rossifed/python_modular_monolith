from shared.di import DIContainer
from shared.events import Event, EventDispatcher


class DefaultEventDispatcher(EventDispatcher):
    """Simple event dispatcher using DI container"""

    def __init__(self, container: DIContainer):
        self.container = container

    async def dispatch(self, event: Event) -> None:
        """Dispatch a event to its handler"""
        event_type = type(event)

        # Resolve handler directly by event type from DI container
        handler = self.container.resolve(event_type)
        await handler.handle(event)
