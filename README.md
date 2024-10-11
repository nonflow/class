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

```bash
python runner.py commands.yaml
```

Make sure you have a `commands.yaml` file in the same directory with the list of commands you want to execute.

## Dependencies

- PyYAML: Used for parsing YAML files.

## Configuration

1. Create a `private.yaml` file with the necessary account information for authentication.
2. Modify the `commands.yaml` file to include the commands you want to execute.

## Note

This project is designed to be extensible. You can add new modules and methods by creating new Python files and updating the `runner.py` script to import them.

## License

Please refer to the LICENSE file in the project repository for licensing information.
