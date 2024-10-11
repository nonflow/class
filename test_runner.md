# test_runner.py Documentation

## Overview
`test_runner.py` is a Python script that contains unit tests for the `runner.py` module. It uses the `unittest` framework to test various functions and the main execution flow of the runner script.

## Purpose
The purpose of this script is to ensure the correct functionality of the `runner.py` module by testing its individual components and the overall execution flow. It helps maintain the reliability and correctness of the command runner system.

## Main Components

1. `TestRunner` class:
   - This is the main test class that inherits from `unittest.TestCase`.
   - It contains several test methods, each focusing on a specific aspect of the `runner.py` module.

2. Test methods:
   - `test_load_yaml()`: Tests the YAML loading functionality.
   - `test_list_classes_and_objects()`: Tests the dynamic class and object listing.
   - `test_execute_command()`: Tests the command execution functionality.
   - `test_main()`: Tests the main execution flow of the runner script.
   - `test_execute_sql_query()`: Tests the new SQL query execution functionality.

## Test Cases

1. `test_load_yaml()`:
   - Mocks the file opening process.
   - Tests if the `load_yaml()` function correctly parses a simple YAML structure.

2. `test_list_classes_and_objects()`:
   - Mocks the module importing process.
   - Checks if the function correctly identifies and lists classes and methods from the mocked modules.

3. `test_execute_command()`:
   - Creates a mock class and object structure.
   - Tests if the `execute_command()` function correctly calls the specified method and prints the result.

4. `test_main()`:
   - Mocks the command-line arguments, YAML loading, and class listing processes.
   - Tests the overall flow of the `main()` function, including command execution and output printing.

5. `test_execute_sql_query()`:
   - Mocks the SQLite connection and cursor.
   - Tests if the `execute_sql_query()` function correctly executes SQL queries and returns results.

## Usage
To run the tests, execute the following command:

```
python -m unittest test_runner.py
```

## Testing SQL Functionality

To test the new SQL functionality in `runner.py`, you can add SQL queries directly in the sentences of your `commands.yaml` file. Here's an example of how to structure a SQL query in the YAML file:

```yaml
commands:
  python:
    sentence:
      - "SELECT * FROM query LIMIT 5"
      - "SELECT service_name, method_name, COUNT(*) as count FROM query GROUP BY service_name, method_name"
```

These SQL queries will be executed against the SQLite database specified by the `DB_PATH` in `runnerdb.py`.

To manually test the SQL functionality:

1. Ensure you have some data in your SQLite database.
2. Run the `runner.py` script with a SQL query:
   ```
   python runner.py "SELECT * FROM query LIMIT 5"
   ```
3. The script should execute the SQL query and print the results in a tabular format.

## Dependencies
- unittest: Python's built-in testing framework.
- unittest.mock: For creating mock objects and patching functions during testing.
- sys: For manipulating command-line arguments in tests.
- io: For capturing stdout in tests.
- sqlite3: For testing SQL query execution.

## Notes
- The tests use extensive mocking to isolate the functionality of `runner.py` and avoid dependencies on actual file systems or module imports.
- The `patch` decorator is used to mock various functions and objects, allowing for controlled testing environments.
- The tests cover both successful scenarios and error handling in the `runner.py` module.
- The new SQL functionality allows for direct execution of SQL queries against the SQLite database, providing a powerful way to retrieve and analyze stored data.

## Importance
These unit tests are crucial for maintaining the integrity of the `runner.py` module. They help catch potential bugs introduced by code changes and ensure that the core functionality of the command runner system remains intact across updates and modifications. The addition of SQL query support enhances the system's capabilities for data retrieval and analysis.
