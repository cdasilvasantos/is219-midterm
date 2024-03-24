"""
Tests for the App module.
"""

import logging
import multiprocessing
import pytest
from app import App


# Define start_app function
def start_app(input_queue):
    """Function to start the App instance in a separate process."""
    app = App()
    app.command_handler.execute_command = lambda _: input_queue.get()  # Override execute_command to read from input_queue
    app.start()

# Disable logging during testing
logging.disable(logging.CRITICAL)

def test_multiprocessing(caplog):
    """Test that the application runs in multiple processes."""
    caplog.set_level(logging.INFO)  # Set logging level to INFO to capture log messages
    input_queue = multiprocessing.Queue()

    process = multiprocessing.Process(target=start_app, args=(input_queue,))
    process.start()

    process.join(timeout=2)

    assert not process.is_alive()

def test_app_start_exit_command(capfd, monkeypatch, caplog):
    """Test that the REPL exits correctly on 'exit' command."""
    caplog.set_level(logging.INFO)  # Set logging level to INFO to capture log messages
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    with pytest.raises(SystemExit):
        App().start()

def test_app_start_unknown_command(capfd, monkeypatch, caplog):
    """Test how the REPL handles an unknown command before exiting."""
    caplog.set_level(logging.ERROR)  # Set logging level to ERROR to capture error messages
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        App().start()
