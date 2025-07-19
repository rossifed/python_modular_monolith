from typing import Protocol
from shared.messaging.abstractions import MessageBroker
from shared.logging.abstractions import Logger
from market_data.application.events import MarketDataEvent
from market_data.application.commands import CreateMarketData
from market_data.application.dto import MarketDataDto


class MarketDataService(Protocol):

    async def publish_market_data(self,
                                  market_data_event: MarketDataEvent) -> None:
        ...


class DummyMarketDataService(MarketDataService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def publish_market_data(self, command: CreateMarketData):
        await self.message_broker.publish_async(
            MarketDataEvent(MarketDataDto(command.symbol, command.price))
            )
