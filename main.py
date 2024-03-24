import sys
import os
import pandas as pd
from decimal import Decimal, InvalidOperation
from app.commands import CommandHandler
from app.plugins.menu import MenuCommand
from app.plugins.discord import DiscordCommand
from app.plugins.email import EmailCommand
from app.plugins.goodbye import GoodbyeCommand
from app.plugins.greet import GreetCommand
from datetime import datetime 

# Function to save history to a CSV file
def save_history_to_csv(history):
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)  # Create the data folder if it doesn't exist
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f'calculation_history_{timestamp}.csv'
    csv_path = os.path.join(data_folder, csv_filename)
    df = pd.DataFrame(history, columns=['Calculation'])
    df.to_csv(csv_path, index=False)
    return csv_path

def load_history_from_csv():
    csv_path = os.path.join('data', 'calculation_history.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df['Calculation'].tolist()
    else:
        return []

# Function to clear history
def clear_history():
    csv_path = os.path.join('data', 'calculation_history.csv')
    if os.path.exists(csv_path):
        os.remove(csv_path)

# Function to delete a specific calculation from history
def delete_calculation(index):
    csv_path = os.path.join('data', 'calculation_history.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if 0 <= index < len(df):
            df.drop(index=index, inplace=True)
            df.to_csv(csv_path, index=False)

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
        
        # Save history to CSV
        save_history_to_csv(history)
    else:
        print("No history of calculations available.")


def display_plugins(command_handler):
    # Retrieve the available plugins and their commands
    plugins = command_handler.commands.keys()
    print("Available plugins:")
    for plugin_name in plugins:
        print(plugin_name)

def main():
    command_handler = CommandHandler()  # Create CommandHandler instance
    menu_command = MenuCommand(command_handler)

    discord_command = DiscordCommand()
    command_handler.register_command('discord', discord_command)

    email_command = EmailCommand()
    command_handler.register_command('email', email_command)

    goodbye_command = GoodbyeCommand()
    command_handler.register_command('goodbye', goodbye_command)

    greet_command = GreetCommand()
    command_handler.register_command('greet', greet_command)

    if len(sys.argv) > 1 and sys.argv[1] != 'exit':
        args = sys.argv[1:]  # Exclude the script name
        calculate_and_print(*args, command_handler)  # Call calculate_and_print directly with provided arguments and command_handler
        return

    while True:
        user_input = input("Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: ")

        if user_input.strip().lower() == 'exit':
            break

        if user_input.strip().lower() == 'history':
            display_history(command_handler)
            continue

        if user_input.strip().lower() == 'menu':
            # Execute the MenuCommand
            menu_command.execute()
            continue

        if user_input.strip().lower() == 'plugins':
            display_plugins(command_handler)  # Call display_plugins with command_handler argument
            continue

        # Check if the input matches any of the registered plugin names
        if user_input.strip().lower() in command_handler.commands:
            command_handler.execute_command(user_input.strip().lower())
            continue

        # Handle expressions like "5+5"
        if '+' in user_input:
            parts = user_input.split('+')
            if len(parts) == 2:
                a, b = parts
                calculate_and_print(a, b, 'add', command_handler)
                continue

                # Check if the input starts with 'delete'
        if user_input.strip().lower().startswith('delete '):
            try:
                # Extract the index from the user input
                index = int(user_input.strip().lower().split(' ')[1])
                # Delete the calculation at the specified index
                delete_calculation(index - 1)
                print("Calculation deleted successfully.")
                continue  # Skip the rest of the loop iteration
            except IndexError:
                print("Invalid index.")
            except ValueError:
                print("Invalid index format. Please enter a valid integer.")

        try:
            a, b, operation_name = user_input.split()
            calculate_and_print(a, b, operation_name, command_handler)  # Pass command_handler
        except ValueError:
            print("Invalid input. Please enter in the format 'number1 number2 operation'.")

    print("Exiting program.")




if __name__ == '__main__':
    main()
