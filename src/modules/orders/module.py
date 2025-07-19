from fastapi import FastAPI
from shared.di.abstractions import DIContainer
from orders.application.commands import CreateOrder
from orders.application.commands.handlers import CreateOrderHandler
from orders.application.events.handlers import MarketDataEventHandler
from orders.application.events import MarketDataEvent
from shared.modules.abstractions import HandlerRegistrar
from orders.application.queries.order_query import OrderQuery
from orders.application.queries.handlers import OrderQueryHandler


class OrdersModule:
    def __init__(self):
        self.name = "orders"
        self.enabled = True

    def register_services(self, container: DIContainer) -> None:
        print(f"✅ Services registered for module '{self.name}'")
        container.add_scoped(CreateOrder, CreateOrderHandler)
        container.add_scoped(OrderQuery, OrderQueryHandler)

    def register_handlers(self, hander_registration: HandlerRegistrar) -> None:
        print(f"✅ Services registered for module '{self.name}'")
        hander_registration.register(MarketDataEvent, MarketDataEventHandler)

    def boot(self, app: FastAPI) -> None:
        """Initialisation du module"""
        print(f"✅ Module '{self.name}' booted")
