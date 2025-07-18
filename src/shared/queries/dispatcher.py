from shared.di.abstractions import DIContainer
from shared.queries.abstractions import Query, R, QueryDispatcher


class DefaultQueryDispatcher(QueryDispatcher):
    """Simple query dispatcher using DI container"""

    def __init__(self, container: DIContainer):
        self.container = container

    async def dispatch(self, query: Query[R]) -> R:
        """Dispatch a query to its handler"""
        query_type = type(query)

        # Resolve handler directly by query type from DI container
        handler = self.container.resolve(query_type)
        return await handler.handle(query)
