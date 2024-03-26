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
import logging
import logging.config

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log')

# Function to save history to a CSV file
def save_history_to_csv(history):
    try:
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)  # Create the data folder if it doesn't exist
        csv_path = os.path.join(data_folder, 'calculation_history.csv')
        
        # Filter out "DELETED" calculations before saving to CSV
        filtered_history = [calculation for calculation in history if not calculation.endswith('DELETED')]
        
        df = pd.DataFrame({'Calculations': filtered_history})
        df.to_csv(csv_path, index=False)
        logging.info("Calculation history saved to CSV.")
    except Exception as e:
        logging.error(f"Error saving calculation history to CSV: {e}")


def load_history_from_csv():
    try:
        csv_path = os.path.join('data', 'calculation_history.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Filter out "DELETED" calculations before returning the history
            history = df[df['Calculation'] != 'DELETED']['Calculation'].tolist()
            return history
        else:
            return []
    except Exception as e:
        logging.error(f"Error loading calculation history from CSV: {e}")
        return []

# Function to save deleted calculations to a CSV file
def save_deleted_to_csv(deleted_calculation):
    try:
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)  # Create the data folder if it doesn't exist
        csv_path = os.path.join(data_folder, 'deleted_calculations.csv')

        df = pd.DataFrame({'Deleted Calculations': [deleted_calculation]})
        df.to_csv(csv_path, mode='a', index=False, header=not os.path.exists(csv_path))
        logging.info("Deleted calculation saved to CSV.")
    except Exception as e:
        logging.error(f"Error saving deleted calculation to CSV: {e}")

# Function to clear history
def clear_history():
    try:
        csv_path = os.path.join('data', 'calculation_history.csv',)
        deleted_csv_path = os.path.join('data', 'deleted_calculations.csv')
        if os.path.exists(csv_path):
            os.remove(csv_path)
            logging.info("Calculation history cleared.")
        if os.path.exists(deleted_csv_path):
            os.remove(deleted_csv_path)
            logging.info("Deleted calculation history cleared.")
    except Exception as e:
        logging.error(f"Error clearing calculation history: {e}")


def delete_calculation(index, command_handler):
    try:
        history = command_handler.get_history()
        if 0 <= index < len(history):
            deleted_calculation = history.pop(index)
            save_deleted_to_csv(deleted_calculation)
            save_history_to_csv(history)
            logging.info("Calculation marked as deleted.")
            return True
    except Exception as e:
        logging.error(f"Error deleting calculation: {e}")
    return False

def calculate_and_return(a, b, operation_name, command_handler):
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

        # Add the calculation to the history if it's not marked as deleted
        if not calculation_str.endswith('DELETED'):
            command_handler.add_to_history(calculation_str)

        # Save the history to CSV after each calculation
        save_history_to_csv(command_handler.get_history())

        return result

    except InvalidOperation:
        logging.error(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError as e:
        logging.error(f"Error: {e}")
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def display_history(command_handler):
    try:
        # Retrieve the history of calculations
        history = command_handler.get_history()

        if history:
            print("History of calculations:")
            for index, calculation in enumerate(history, start=1):
                # Check if the calculation does not end with "DELETED"
                if not calculation.endswith('DELETED'):
                    print(f"{index}. {calculation}")
        else:
            print("No history of calculations available.")
    except Exception as e:
        logging.error(f"Error displaying history: {e}")


def display_plugins(command_handler):
    try:
        # Retrieve the available plugins and their commands
        plugins = command_handler.commands.keys()
        print("Available plugins:")
        for plugin_name in plugins:
            print(plugin_name)
    except Exception as e:
        logging.error(f"Error displaying plugins: {e}")

def main():
    try:
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
            result = calculate_and_return(*args, command_handler)  # Call calculate_and_print directly with provided arguments and command_handler
            print(f"The result of the calculation is {result}")
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
            if ' ' in user_input:
                parts = user_input.split()
                if len(parts) == 3:
                    a, b, operation_name = parts
                    if operation_name in ['add', 'subtract', 'multiply', 'divide']:
                        result = calculate_and_return(a, b, operation_name, command_handler)
                        if result is not None:
                            print(f"The result of the calculation is {result}")
                        continue
                    else:
                        print("Invalid input: please enter a valid operation (add, subtract, multiply, divide)")
                        continue

            # Check if the input is 'save'
            if user_input.strip().lower() == 'save':
                logging.warning("'save' command not supported in this context.")
                continue
            
            # Check if the input is 'clear'
            if user_input.strip().lower() == 'clear':
                clear_history()
                continue

            # Check if the input starts with 'delete'
            if user_input.strip().lower().startswith('delete '):
                try:
                    # Extract the index from the user input
                    index = int(user_input.strip().lower().split(' ')[1])
                    # Delete the calculation at the specified index
                    deleted = delete_calculation(index - 1, command_handler)
                    if deleted:
                        print(f"Deleted calculation at index {index}")
                        display_history(command_handler)  # Reload history after successful deletion
                    continue  # Skip the rest of the loop iteration
                except IndexError:
                    logging.error("Invalid index.")
                except ValueError:
                    logging.error("Invalid index format. Please enter a valid integer.")


            logging.error("Invalid input. Please enter a valid command.")

        logging.info("Exiting program.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
