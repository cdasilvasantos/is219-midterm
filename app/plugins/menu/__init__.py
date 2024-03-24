import logging
from app.commands import Command
import importlib
import pkgutil

class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def execute(self, args=None):
        logging.info("Available plugins:")
        print("Available plugins:")

        # Import modules from the 'app.plugins' package
        plugins_package = 'app.plugins'
        for _, module_name, _ in pkgutil.iter_modules([plugins_package]):
            module = importlib.import_module(f'{plugins_package}.{module_name}')
            print(module_name)
            logging.info(module_name)

        print("Type 'exit' to exit.")
