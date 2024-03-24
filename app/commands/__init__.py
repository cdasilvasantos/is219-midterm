from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name: str, *args):
        """ Execute the given command with optional arguments."""
        command = self.commands.get(command_name)
        if command:
            command.execute(*args)
        else:
            print(f"No such command: {command_name}")
