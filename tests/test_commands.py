"""
Module: test_commands.py
This module contains unit tests for the commands in the App class.
"""
import pytest
from app import App



def test_app_menu_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'menu' command."""
    # Simulate user entering 'menu' followed by 'exit'
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    assert e.type == SystemExit
    assert e.value.code == 0  # Check if the exit code is 0
