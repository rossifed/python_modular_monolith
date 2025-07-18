from shared.events.abstractions import EventHandler
from orders.application.events.market_data_event import MarketDataEvent


class MarketDataEventHandler(EventHandler[MarketDataEvent]):
    async def handle(self, event: MarketDataEvent) -> None:
        print(f"Market Data Received: {event.symbol} {event.price}")
