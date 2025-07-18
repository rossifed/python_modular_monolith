from shared.commands.abstractions import CommandHandler
from market_data.application.commands import CreateUserCommand
from shared.logging.abstractions import Logger
from market_data.application.services.market_data_service import (
     MarketDataService)


class CreateUserHandler(CommandHandler[CreateUserCommand]):
    def __init__(self, market_data_service: MarketDataService, logger: Logger):
        self.market_data_service = market_data_service
        self.logger = logger

    async def handle(self, command: CreateUserCommand) -> None:
        self.logger.info(f"Creating user {command.name}")
        await self.market_data_service.do_something()
