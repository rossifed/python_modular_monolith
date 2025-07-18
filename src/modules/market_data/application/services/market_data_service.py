from typing import Protocol
from shared.messaging.abstractions import MessageBroker
from shared.logging.abstractions import Logger
from market_data.application.events.market_data_event import MarketDataEvent


class MarketDataService(Protocol):

    async def do_something_async(self) -> None:
        ...


class DummyMarketDataService(MarketDataService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def do_something(self, ):
        market_data_event = MarketDataEvent("BTCUSD", 12.5)
        await self.message_broker.publish_async(market_data_event)
