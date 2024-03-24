import sys
from decimal import Decimal, InvalidOperation
from app import App
from app.commands import CommandHandler

def calculate_and_print(a, b, operation_name, command_handler):
    try:
        a_decimal, b_decimal = Decimal(a), Decimal(b)
        if operation_name == 'add':
            result = a_decimal + b_decimal
        elif operation_name == 'subtract':
            result = a_decimal - b_decimal
        elif operation_name == 'multiply':
            result = a_decimal * b_decimal
        elif operation_name == 'divide':
            if b_decimal == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            result = a_decimal / b_decimal
        else:
            raise ValueError(f"Unknown operation: {operation_name}")

        # Create a calculation string
        calculation_str = f"{a} {operation_name} {b} = {result}"

        # Add the calculation to the history
        command_handler.add_to_history(calculation_str)

        # Print the result
        print(f"The result of {calculation_str}")

    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def display_history(command_handler):
    # Retrieve the history of calculations
    history = command_handler.get_history()

    if history:
        print("History of calculations:")
        for index, calculation in enumerate(history, start=1):
            print(f"{index}. {calculation}")
    else:
        print("No history of calculations available.")



def display_plugins():
    App().command_handler.execute_command('plugins')

def main():
    command_handler = CommandHandler()  # Create CommandHandler instance
    command_handler.register_command('calculate_and_print', calculate_and_print)  # Register the calculate_and_print command
    command_handler.register_command('history', display_history)  # Register the history command

    if len(sys.argv) > 1 and sys.argv[1] != 'exit':
        args = sys.argv[1:]  # Exclude the script name
        calculate_and_print(*args, command_handler)  # Call calculate_and_print directly with provided arguments and command_handler
        return

    while True:
        user_input = input("Enter calculation, 'menu' to view available plugins, 'history' to view history, or 'exit' to quit: ")

        if user_input.strip().lower() == 'exit':
            break

        if user_input.strip().lower() == 'history':
            display_history(command_handler)
            continue

        if user_input.strip().lower() == 'plugins':
            display_plugins()
            continue

        # Handle expressions like "5+5"
        if '+' in user_input:
            parts = user_input.split('+')
            if len(parts) == 2:
                a, b = parts
                calculate_and_print(a, b, 'add', command_handler)
                continue

        try:
            a, b, operation_name = user_input.split()
            calculate_and_print(a, b, operation_name, command_handler)  # Pass command_handler
        except ValueError:
            print("Invalid input. Please enter in the format 'number1 number2 operation'.")

    print("Exiting program.")

if __name__ == '__main__':
    main()
