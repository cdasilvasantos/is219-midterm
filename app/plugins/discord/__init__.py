import logging
import sys
from app.commands import Command


class DiscordCommand(Command):
    def execute(self):
        logging.info("I will send something on discord")
        print(f'I will send something on discord')