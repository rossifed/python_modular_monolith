from shared.commands.abstractions import Command


class CreateOrderCommand(Command):
    def __init__(self, name: str):
        self.name = name
