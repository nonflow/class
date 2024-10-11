# Run Command by Sentences
```bash
_   _             _____ _               
| \ | |           |  ___| |              
|  \| | ___  _ __ | |_  | | _____      __
| . ` |/ _ \| '_ \|  _| | |/ _ \ \ /\ / /
| |\  | (_) | | | | |   | | (_) \ V  V /
\_| \_/\___/|_| |_\_|   |_|\___/ \_/\_/
```

![NonFlow Logo](logo/nonflow.svg)

This project implements a flexible command runner system that dynamically loads and executes commands from a YAML file. It includes functionality for interacting with various services such as Cloudflare, GitLab, GitHub, and Plesk, and stores the results in a SQLite database.

## Project Structure

The project consists of the following main components:

1. `runner.py`: The main script that orchestrates the command execution process.
2. `runnerdb.py`: Imports database operations from the src folder.
3. `src/`: Directory containing individual function files for both runner.py and runnerdb.py operations.
4. `python/`: Directory containing service classes (e.g., CloudflareService, GitLabService, GitHubService, PleskService).
5. `commands.yaml`: Contains the list of commands to be executed by the runner.
6. `.private`: Stores sensitive information like API keys and tokens.
7. `.env`: Contains environment variables for configuring file paths, database settings, and logging.
8. `requirements.txt`: Lists the Python dependencies for the project.
9. `logo/`: Directory containing logo files for the project.
10. `.logs`: Log file containing detailed execution logs.
11. `tests/`: Directory containing unit tests for the project.
12. `run_tests.sh`: Bash script to run unit tests.
13. `TESTING.md`: Documentation for running and writing tests.

## How It Works

1. The `runner.py` script is the entry point of the application. It does the following:
   - Loads environment variables from the `.env` file.
   - Loads commands from the specified YAML file.
   - Loads service configuration from `.private`.
   - Dynamically imports and recognizes all service classes in the `python/` directory.
   - Lists available classes and their methods.
   - Executes the commands specified in the YAML file using functions from the `src/` directory.
   - Stores the results of each command in the SQLite database.
   - Logs detailed information about the execution process to the `.logs` file.

2. Each service class provides methods for interacting with their respective APIs.

3. The `runnerdb.py` script imports database operations from the `src/` directory, including:
   - Initializing the database and creating necessary tables.
   - Saving command results to the database.
   - Retrieving the latest results for a given service and method.

4. The `src/` directory contains individual Python files for each function used in `runner.py` and `runnerdb.py`. This modular structure improves code organization and maintainability.

[The rest of the README.md content remains the same]
