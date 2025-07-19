from shared.events.abstractions import Event
from dataclasses import dataclass
from market_data.application.dto import MarketDataDto


@dataclass(frozen=True)
class MarketDataEvent(Event):
    market_data: MarketDataDto
