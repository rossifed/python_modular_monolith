from fastapi import FastAPI
from shared.di.abstractions import DIContainer
from market_data.application.services.market_data_service import (
    MarketDataService,
    DummyMarketDataService
)
from market_data.application.query_handlers import HelloQueryHandler
from market_data.application.queries import HelloQuery
from shared.messaging.abstractions import MessageBroker
from shared.logging.abstractions import Logger
from market_data.application.command_handlers import CreateUserHandler
from market_data.application.commands import CreateUserCommand
from shared.modules.abstractions import HandlerRegistrar


class MarketDataModule:
    def __init__(self):
        self.name = "market_data"
        self.enabled = True

    def register_services(self, container: DIContainer) -> None:
        container.add_singleton(MarketDataService,
                                lambda: DummyMarketDataService(
                                    container.resolve(MessageBroker),
                                    container.resolve(Logger)
                                ))

    def register_handlers(self, handler_registrar: HandlerRegistrar) -> None:
        handler_registrar.register(HelloQuery, HelloQueryHandler)
        handler_registrar.register(CreateUserCommand,
                                   lambda c: CreateUserHandler(
                                    c.resolve(MarketDataService),
                                    c.resolve(Logger)
                                    ))

    def boot(self, app: FastAPI) -> None:
        """Initialisation du module"""
        print(f"✅ Module '{self.name}' booted")
