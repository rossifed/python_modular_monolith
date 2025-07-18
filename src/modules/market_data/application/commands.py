from shared.commands.abstractions import Command


class CreateUserCommand(Command):
    def __init__(self, name: str):
        self.name = name
