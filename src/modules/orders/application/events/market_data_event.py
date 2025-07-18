from shared.events.abstractions import Event
from dataclasses import dataclass


@dataclass
class MarketDataEvent(Event):
    symbol: str
    price: float
