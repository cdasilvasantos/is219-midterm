"""
Test file for the calculate_and_return function
"""

from main import calculate_and_return

class MockCommandHandler:
    """
    Mock class for CommandHandler
    """

    def __init__(self):
        self.history = []

    def add_to_history(self, calculation):
        """
        Mock method to add a calculation to history
        """
        self.history.append(calculation)

    def get_history(self):
        """
        Mock method to retrieve calculation history
        """
        return self.history

def test_calculate_and_return():
    """
    Test the calculate_and_return function with different scenarios
    """
    # Create a mock CommandHandler instance
    command_handler = MockCommandHandler()

    # Test addition
    assert calculate_and_return(5, 3, 'add', command_handler) == 8

    # Test subtraction
    assert calculate_and_return(5, 3, 'subtract', command_handler) == 2

    # Test multiplication
    assert calculate_and_return(5, 3, 'multiply', command_handler) == 15

    # Test division
    assert calculate_and_return(10, 2, 'divide', command_handler) == 5

    # Test division by zero
    assert calculate_and_return(5, 0, 'divide', command_handler) is None

    # Test invalid operation
    assert calculate_and_return(5, 3, 'invalid', command_handler) is None

    # Test invalid numbers
    assert calculate_and_return('invalid', 3, 'add', command_handler) is None
    assert calculate_and_return(5, 'invalid', 'add', command_handler) is None

    # Test calculation history
    assert command_handler.history == [
        '5 add 3 = 8', 
        '5 subtract 3 = 2', 
        '5 multiply 3 = 15', 
        '10 divide 2 = 5'
    ]
