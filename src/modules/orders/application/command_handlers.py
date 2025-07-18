from shared.commands.abstractions import CommandHandler
from orders.application.commands import CreateOrderCommand


class CreateOrderHandler(CommandHandler[CreateOrderCommand]):
    async def handle(self, command: CreateOrderCommand) -> None:
        print(f"Creating order {command.name}")
