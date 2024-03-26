"""
Tests for CommandHandler class.
"""

# Import the necessary module
from app.commands import CommandHandler

# Define a simple class with an execute method
class SimpleCommand:
    """A simple command class."""
    def execute(self):
        """Execute the command."""
        return 'Test command executed'

# Test CommandHandler class
class TestCommandHandler:
    """Test suite for the CommandHandler class."""
    # Setup method to create a CommandHandler instance for each test
    def setup_method(self):
        """Setup method to create a CommandHandler instance for each test."""
        # pylint: disable=attribute-defined-outside-init
        self.command_handler = CommandHandler()


    # Test registering commands
    def test_register_command(self):
        """Test registering commands."""
        # Register commands
        self.command_handler.register_command('test_command', SimpleCommand)
        # Verify that the command is registered
        assert 'test_command' in self.command_handler.commands

    # Test executing commands
    def test_execute_command(self):
        """Test executing commands."""
        # Register a test command
        self.command_handler.register_command('test_command', SimpleCommand())
        # Execute the command
        output = self.command_handler.execute_command('test_command')
        # Verify that the command was executed successfully
        assert output == 'Test command executed'

    # Test adding to command history
    def test_add_to_history(self):
        """Test adding to command history."""
        # Add a command to history
        self.command_handler.add_to_history('test_command')
        # Verify that the command is added to history
        assert 'test_command' in self.command_handler.get_history()
