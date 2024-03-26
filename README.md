## IS 219 Midterm Documentation

## Video Demonstration
https://youtu.be/DNcUObGjdcg

### Description
The Advanced Python Calculator Application is a comprehensive project developed as part of the IS 219 class's midterm assessment. The primary goal of this project is to demonstrate proficiency in professional software development practices by integrating various advanced concepts and techniques learned throughout the course.

#### Key Features:

* Clean, Maintainable Code: The application is built with a focus on writing clean, modular, and maintainable code following best practices and coding standards.
* Design Patterns: Design patterns, such as the Command Handler pattern and Plugin Architecture, are employed to promote code reusability, extensibility, and maintainability.
* Comprehensive Logging: Logging is implemented using Python's logging module to facilitate effective debugging, error tracking, and monitoring of application events.
* Dynamic Configuration: Configuration parameters are managed via environment variables, allowing for easy customization and deployment across different environments.
* Data Handling with Pandas: The application leverages the power of Pandas for sophisticated data manipulation, particularly for handling calculation history stored in CSV files.
* Command-Line Interface (REPL): A command-line interface is provided for real-time user interaction, allowing users to input mathematical expressions, view calculation history, and perform various operations seamlessly.

#### Integration of Homework Assignments:
The project integrates concepts and techniques covered in homework assignments, including but not limited to:
* Mathematical operations (addition, subtraction, multiplication, division)
* Implementation of plugins for additional functionalities (e.g., discord, email)
* Implementing adaptable and informative logging
* Testing methodologies to ensure code correctness and reliability

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```bash
   python main.py
   ```

### Usage Examples
1. **Perform Calculations:**
   - Run the application and input mathematical expressions.
   ```bash
   Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: 5 3 add
   The result of the calculation is 8
   Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: 10 4 subtract
   The result of the calculation is 6
   ```
2. **View Calculation History:**
   - Input `history` to view a list of previous calculations.
   ```bash
   Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: history
   History of calculations:
   1. 5 add 3 = 8
   2. 10 subtract 4 = 6
   ```
3. **Delete Calculation:**
   - Input `delete <index>` to delete a specific calculation from history.
   ```bash
   Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: delete 1
   Deleted calculation at index 1
   History of calculations: 
   1. 10 subtract 4 = 6
   ```
4. **Plugin Implementation:**
    - Input `menu` to view a list of available plugins.
    ```bash
    Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: menu
    Available commands:
    discord
    email
    goodbye
    greet
    ```
    - Input any of the plugins above to receive a command.
    ```bash
    Enter a calculation, 'menu' to view available plugins, 'history' to view calculation history, or 'exit' to quit: discord
    I will send something on discord  
    ```

### Architectural Decisions and Design Patterns
1. **Command Handler Pattern:**
   - The project utilizes the Command Handler pattern to decouple the execution of commands from their implementation. This allows for easy extension and modification of commands without impacting the core logic.
2. **Plugin Architecture:**
   - Commands such as `discord`, `email`, `greet`, and `goodbye` are implemented as plugins. This design allows for modularization and easy addition/removal of functionality.
3. **Logging Strategy:**
   - The application employs a logging strategy using Python's built-in logging module. Log messages are categorized by severity levels and formatted with timestamps for easy debugging and monitoring. The log messages for this application can be found in the [app.log](app.log) file. 
4. **Data Persistence:**
   - Calculation history is stored in CSV files, enabling persistent storage of calculations across application sessions. Deleted calculations are marked but retained for future reference. You will be able to find these files in the [data](data) folder once you input a calculation.

#### Usage of Environment Variables
Environment variables play a crucial role in the project by enabling dynamic configuration, providing a means for customization and flexibility without the need for hardcoding values directly into the codebase. In the implemented solution, environment variables are primarily utilized for managing configuration parameters that may vary across different environments, such as file paths or API keys.

In particular, environment variables are employed for configuring the log file path dynamically. This approach ensures that the log file location can be easily customized based on the environment without requiring modifications to the code. By using environment variables, the project achieves adaptability and ease of configuration, allowing seamless deployment across various environments, including development, staging, and production.

#### Example:
```python
import logging
import logging.config
import os

# Configure logging
logger = logging.getLogger(__name__)
log_file_path = os.getenv('LOG_FILE_PATH', 'app.log')  # Use environment variable or default to 'app.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file_path)

```


### Look Before You Leap (LBYL)
LBYL is a defensive programming approach where you check for conditions before executing an operation to avoid potential errors or exceptions. This approach typically involves using conditionals or checks to ensure that the operation can be performed safely.

#### Example:
```python
if operation_name in ['add', 'subtract', 'multiply', 'divide']:
    # Perform the calculation
    result = calculate_and_return(a, b, operation_name, command_handler)
```
In this snippet, you check if the `operation_name` is one of the supported mathematical operations before proceeding with the calculation. This ensures that the operation is valid and prevents potential errors caused by unsupported operations.

### Easier to Ask for Forgiveness than Permission (EAFP)
EAFP is a coding style where you attempt an operation and handle any resulting exceptions rather than checking beforehand whether the operation will succeed. This approach is based on the principle that it's easier to ask for forgiveness (handle exceptions) than to check for permission (preemptively validate conditions).

#### Example:
```python
try:
    a_decimal, b_decimal = Decimal(a), Decimal(b)
    # Attempt the mathematical operation
    result = a_decimal / b_decimal
except ZeroDivisionError as e:
    logging.error(f"Error: {e}")
```
In this example, you attempt the division operation without checking if `b_decimal` is zero beforehand. If `b_decimal` is zero, it will raise a `ZeroDivisionError`, which is caught and handled within the `except` block. This approach simplifies the code and eliminates the need for explicit conditionals to check for potential errors before executing the operation.

### Implementation Details
1. **CommandHandler Class:**
   - Responsible for registering and executing commands.
2. **Plugin Classes:**
   - Each plugin class implements a specific command (e.g., DiscordCommand, EmailCommand) and encapsulates its behavior.
3. **Logging Configuration:**
   - Logging is configured with a basic configuration, including the logging level, format, and file

### Conclusion
The project demonstrates effective utilization of design patterns and architectural decisions to create a flexible, modular, and robust command-line calculator application. By implementing the Command Handler pattern, Plugin Architecture, and a robust logging strategy, the application achieves a high level of extensibility, maintainability, and reliability. Additionally, the use of CSV files for data persistence ensures that calculation history is preserved across sessions, further enhancing user experience and data integrity. For detailed implementation and code analysis, please refer to the source code and documentation within the repository.
