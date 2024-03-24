import sys
from decimal import Decimal, InvalidOperation
from app import App
from app.commands import CommandHandler

def calculate_and_print(a, b, operation_name):
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

        print(f"The result of {a} {operation_name} {b} is equal to {result}")

    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def display_history():
    App().command_handler.execute_command('history')

def display_plugins():
    App().command_handler.execute_command('plugins')

def main():
    command_handler = CommandHandler()  # Create CommandHandler instance
    command_handler.register_command('calculate_and_print', calculate_and_print)  # Register the calculate_and_print command

    if len(sys.argv) > 1 and sys.argv[1] != 'exit':
        args = sys.argv[1:]  # Exclude the script name
        calculate_and_print(*args)  # Call calculate_and_print directly with provided arguments
        return

    while True:
        user_input = input("Enter calculation, 'plugins' to view available plugins, 'history' to view history, or 'exit' to quit: ")

        if user_input.strip().lower() == 'exit':
            break

        if user_input.strip().lower() == 'history':
            display_history()
            continue

        if user_input.strip().lower() == 'plugins':
            display_plugins()
            continue

        try:
            a, b, operation_name = user_input.split()
            calculate_and_print(a, b, operation_name)
        except ValueError:
            print("Invalid input. Please enter in the format 'number1 number2 operation'.")

    print("Exiting program.")

if __name__ == '__main__':
    main()
