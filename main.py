import sys
from decimal import Decimal, InvalidOperation
from app import App

def calculate_and_print(a, b, operation_name):
    try:
        a_decimal, b_decimal = Decimal(a), Decimal(b)
        result = App().command_handler.execute_command(operation_name, a_decimal, b_decimal)  # Pass operation_name along with operands
        print(f"The result of {a} {operation_name} {b} is equal to {result}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def display_history():
    App().command_handler.execute_command('history')

def display_plugins():
    App().command_handler.execute_command('plugins')

def main():
    while True:
        user_input = input("Enter calculation, 'history' to view history, 'plugins' to view available plugins, or 'exit' to quit: ")

        if user_input.strip().lower() == 'exit':
            break
        elif user_input.strip().lower() == 'history':
            display_history()
        elif user_input.strip().lower() == 'plugins':
            display_plugins()
        else:
            try:
                a, b, operation_name = user_input.split()
                calculate_and_print(a, b, operation_name)
            except ValueError:
                print("Invalid input. Please enter in the format 'number1 number2 operation'.")

    print("Exiting program.")

if __name__ == '__main__':
    main()
