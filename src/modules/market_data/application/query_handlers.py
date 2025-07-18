from shared.queries.abstractions import QueryHandler
from market_data.application.queries import HelloQuery


class HelloQueryHandler(QueryHandler[HelloQuery, str]):
    async def handle(self, query: HelloQuery) -> str:
        return f"Hello, {query.name}!"
