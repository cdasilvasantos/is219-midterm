import sys
from decimal import Decimal, InvalidOperation
from calculator import Calculator, Calculations
from calculator.calculation import Calculation

class OperationCommand:
    def __init__(self, calculator, operation_name, a, b):
        self.calculator = calculator
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.result = None  # Initialize result attribute

    def execute(self):
        operation_method = getattr(self.calculator, self.operation_name, None)
        if operation_method:
            self.result = operation_method(self.a, self.b)  # Store the result of the operation
        else:
            raise ValueError(f"Unknown operation: {self.operation_name}")

        return self.result  # Return the result of the operation

def calculate_and_print(a, b, operation_name):
    try:
        a_decimal, b_decimal = Decimal(a), Decimal(b)
        command = OperationCommand(Calculator, operation_name, a_decimal, b_decimal)
        result = command.execute()
        
        # Add the calculation to the history only if the operation was successful
        Calculations.add_calculation(Calculation.create(a_decimal, b_decimal, getattr(Calculator, operation_name)))

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
    history = Calculations.get_history()
    if not history:
        print("No calculations in history.")
    else:
        print("Calculation History:")
        for index, calculation in enumerate(history, start=1):
            operation_name = getattr(calculation.operation, '__name__', 'Unknown')
            print(f"{index}. Calculation({calculation.a}, {calculation.b}, {operation_name})")

def main():
    while True:
        user_input = input("Enter calculation, 'history' to view history, or 'exit' to quit: ")

        if user_input.strip().lower() == 'exit':
            break

        if user_input.strip().lower() == 'history':
            display_history()
            continue

        try:
            a, b, operation_name = user_input.split()
            calculate_and_print(a, b, operation_name)
        except ValueError:
            print("Invalid input. Please enter in the format 'number1 number2 operation'.")

    print("Exiting program.")

if __name__ == '__main__':
    main()
