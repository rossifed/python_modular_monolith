from shared.dispatching.abstractions import Dispatcher as DispatcherProtocol
from shared.commands.abstractions import Command
from shared.events.abstractions import Event
from shared.queries.abstractions import Query
from shared.commands.command_dispatcher import CommandDispatcher
from shared.events.default_event_dispatcher import EventDispatcher
from shared.queries.dispatcher import QueryDispatcher


class DefaultDispatcher(DispatcherProtocol):
    """Default unified dispatcher implementation"""

    def __init__(self,
                 command_dispatcher: CommandDispatcher,
                 event_dispatcher: EventDispatcher,
                 query_dispatcher: QueryDispatcher):
        self._commands = command_dispatcher
        self._events = event_dispatcher
        self._queries = query_dispatcher

    async def send_async(self, command: Command) -> None:
        await self._commands.dispatch(command)

    async def publish_async(self, event: Event) -> None:
        await self._events.dispatch(event)

    async def query_async(self, query: Query) -> any:
        return await self._queries.dispatch(query)
