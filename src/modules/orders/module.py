from fastapi import FastAPI
from shared.di.abstractions import DIContainer
from orders.application.command_handlers import CreateOrderHandler
from orders.application.commands import CreateOrderCommand
from orders.application.events.market_data_event_handler import (
    MarketDataEventHandler)
from orders.application.events.market_data_event import MarketDataEvent
from shared.modules.abstractions import HandlerRegistrar
from orders.application.queries import OrderQuery
from orders.application.query_handlers import OrderQueryHandler


class OrdersModule:
    def __init__(self):
        self.name = "orders"
        self.enabled = True

    def register(self, container: DIContainer,
                 hander_registration: HandlerRegistrar) -> None:
        print(f"✅ Services registered for module '{self.name}'")
        hander_registration.register(MarketDataEvent, MarketDataEventHandler)
        hander_registration.register(MarketDataEvent, MarketDataEventHandler)
        container.add_scoped(CreateOrderCommand, CreateOrderHandler)
        container.add_scoped(OrderQuery, OrderQueryHandler)

    def boot(self, app: FastAPI) -> None:
        """Initialisation du module"""
        print(f"✅ Module '{self.name}' booted")
