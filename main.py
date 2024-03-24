import sys
from decimal import Decimal, InvalidOperation
from calculator import Calculator, Calculations  # Assuming Calculator and Calculations are defined as shown previously

class OperationCommand:
    def __init__(self, calculator, operation_name, a, b):
        self.calculator = calculator
        self.operation_name = operation_name
        self.a = a
        self.b = b

    def execute(self):
        # Retrieve the operation method from the Calculator class using getattr
        operation_method = getattr(self.calculator, self.operation_name, None)
        if operation_method:
            return operation_method(self.a, self.b)
        else:
            raise ValueError(f"Unknown operation: {self.operation_name}")

def calculate_and_print(a, b, operation_name):
    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        result = OperationCommand(Calculator, operation_name, a_decimal, b_decimal).execute()
        print(f"The result of {a} {operation_name} {b} is equal to {result}")
        
        # Add the calculation to the history
        Calculations.add_calculation(Calculation.create(a_decimal, b_decimal, operation_name, result))
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
            print(f"{index}. {calculation}")

def main():
    if len(sys.argv) == 4:
        _, a, b, operation_name = sys.argv
        calculate_and_print(a, b, operation_name)
    else:
        print("Usage: python calculator_main.py <number1> <number2> <operation>")
        print("To view calculation history, use 'history' as the operation.")
        user_input = input("Enter calculation or 'history': ")
        if user_input.strip().lower() == 'history':
            display_history()
        else:
            try:
                a, b, operation_name = user_input.split()
                calculate_and_print(a, b, operation_name)
            except ValueError:
                print("Invalid input. Please enter in the format 'number1 number2 operation'.")

if __name__ == '__main__':
    main()
