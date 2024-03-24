import sys
from decimal import Decimal, InvalidOperation
from app.calculator import Calculator
from app import App

class OperationCommand:
    def __init__(self, calculator, operation_name, a, b):
        self.calculator = calculator
        self.operation_name = operation_name
        self.a = a
        self.b = b

    def execute(self):
        operation_method = getattr(self.calculator, self.operation_name, None)
        if operation_method:
            return operation_method(self.a, self.b)
        else:
            raise ValueError(f"Unknown operation: {self.operation_name}")

def calculate_and_print(a, b, operation_name):
    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        command = OperationCommand(Calculator, operation_name, a_decimal, b_decimal)
        result = command.execute()
        print(f"The result of {a} {operation_name} {b} is equal to {result}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) == 1:
        # If no command-line arguments are provided, start the App
        app_instance = App()  # Create an instance of the App class
        app_instance.start()  # Call the start method of the instance
    elif len(sys.argv) == 4:
        # If three command-line arguments are provided, proceed with calculation
        _, a, b, operation_name = sys.argv
        calculate_and_print(a, b, operation_name)
    else:
        print("Usage:")
        print("To start the application: python main.py")
        print("To perform a calculation: python main.py <number1> <number2> <operation>")
        sys.exit(1)

if __name__ == '__main__':
    main()
