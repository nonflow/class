# Command Runner Project

This project implements a flexible command runner system that dynamically loads and executes commands from a YAML file. It includes functionality for managing accounts and messages.

## Project Structure

The project consists of the following main components:

1. `runner.py`: The main script that loads commands from a YAML file and executes them.
2. `Account.py`: Defines the Account class for managing user accounts.
3. `Message.py`: Defines the Message class for creating, reading, listing, and deleting messages.
4. `commands.yaml`: Contains the list of commands to be executed by the runner.
5. `private.yaml`: Stores private data for account authentication (not included in the repository).

## How It Works

1. The `runner.py` script is the entry point of the application. It does the following:
   - Loads commands from the specified YAML file.
   - Dynamically imports the Account and Message modules.
   - Lists available modules and methods.
   - Executes the commands specified in the YAML file.

2. The `Account` class provides methods for:
   - Connecting to an account using an email address.
   - Disconnecting from the current account.

3. The `Message` class provides methods for:
   - Creating new messages with a sender, content, and subject.
   - Reading messages by their ID.
   - Listing messages within a specified date range.
   - Deleting messages by their ID.

## Usage

To run the command runner:

```
python runner.py commands.yaml
```

Make sure you have a `commands.yaml` file in the same directory with the list of commands you want to execute.

## Starting Projects and Running Tests

To start a new project and run tests:

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/command-runner.git
   cd command-runner
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create your `commands.yaml` and `private.yaml` files based on the provided examples.

4. To run tests, use the following command:
   ```
   python -m unittest test_runner.py
   ```

   This will execute the test cases defined in the `test_runner.py` file.

5. To run specific test cases, you can use:
   ```
   python -m unittest test_runner.TestRunnerMethods.test_method_name
   ```

   Replace `test_method_name` with the name of the specific test method you want to run.

6. For continuous testing during development, you can use a tool like `pytest-watch`:
   ```
   pip install pytest-watch
   ptw
   ```

   This will watch for file changes and automatically run tests when you save your files.

## Dependencies

- PyYAML: Used for parsing YAML files.

## Configuration

1. Create a `private.yaml` file with the necessary account information for authentication.
2. Modify the `commands.yaml` file to include the commands you want to execute.

## Note

This project is designed to be extensible. You can add new modules and methods by creating new Python files and updating the `runner.py` script to import them.

## License

Please refer to the LICENSE file in the project repository for licensing information.
