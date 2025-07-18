from shared.queries.abstractions import QueryHandler
from orders.application.queries import OrderQuery


class OrderQueryHandler(QueryHandler[OrderQuery, str]):
    async def handle(self, query: OrderQuery) -> str:
        return f"Order, {query.name}!"
