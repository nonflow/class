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

1. `runner.py`: The main script that loads commands from a YAML file and executes them.
2. `runnerdb.py`: Handles database operations for storing and retrieving command results.
3. `python/`: Directory containing service classes (e.g., CloudflareService, GitLabService, GitHubService, PleskService).
4. `commands.yaml`: Contains the list of commands to be executed by the runner.
5. `.private`: Stores sensitive information like API keys and tokens.
6. `.env`: Contains environment variables for configuring file paths, database settings, and logging.
7. `requirements.txt`: Lists the Python dependencies for the project.
8. `logo/`: Directory containing logo files for the project.
9. `.logs`: Log file containing detailed execution logs.
10. `tests/`: Directory containing unit tests for the project.
11. `run_tests.sh`: Bash script to run unit tests.
12. `TESTING.md`: Documentation for running and writing tests.

## How It Works

1. The `runner.py` script is the entry point of the application. It does the following:
   - Loads environment variables from the `.env` file.
   - Loads commands from the specified YAML file.
   - Loads service configuration from `.private`.
   - Dynamically imports and recognizes all service classes in the `python/` directory.
   - Lists available classes and their methods.
   - Executes the commands specified in the YAML file.
   - Stores the results of each command in the SQLite database.
   - Logs detailed information about the execution process to the `.logs` file.

2. Each service class provides methods for interacting with their respective APIs.

3. The `runnerdb.py` script handles all database operations, including:
   - Initializing the database and creating necessary tables.
   - Saving command results to the database.
   - Retrieving the latest results for a given service and method.

## Command Structure

The `commands.yaml` file has the following structure:

```yaml
commands:
  python:
    sentence:
      - list zones cloudflare_main
      - list projects gitlab_main
      # ... more commands ...
```

Each command specifies the method to call (using spaces instead of underscores) and an account alias that references the service configuration in `.private`.

## Service Configuration

The `.private` file stores sensitive information like API keys and tokens. It has the following structure:

```yaml
cloudflare_main:
  service: CloudflareService
  api_key: your_actual_api_key
  email: your_actual_email@example.com

gitlab_main:
  service: GitLabService
  base_url: https://gitlab.com
  private_token: your_actual_private_token

# ... more services and accounts ...
```

Each account alias contains the service class name and the necessary credentials for that service.

## Environment Variables

The `.env` file is used to set the paths for various configuration files and outputs. It has the following structure:

```
PRIVATE_YAML_PATH=.private/service.yaml
COMMANDS_YAML_PATH=commands.yaml
SQLITE_DB_PATH=runner.db
LOG_FILE_PATH=.logs
```

This allows you to easily change the location of these files and the database without modifying the `runner.py` script.

## Database Usage

The project uses a SQLite database to store the results of each command execution. The database operations are handled by the `runnerdb.py` script, which provides the following functionality:

- Initializing the database and creating the necessary table.
- Saving command results to the database.
- Retrieving the latest result for a given service and method.

The database stores the following information for each command execution:
- Service name
- Method name
- Result (stored as a JSON string)
- Timestamp of the execution

This allows for easy retrieval and analysis of past command executions.

## SQL Queries on JSON and XML Data

The runner now supports executing SQL queries on JSON and XML data stored in the 'result' column of the database. This feature allows for complex data analysis and retrieval directly from the stored results.

### JSON Queries

You can use SQL queries with JSON functions to extract and analyze data from the 'result' column. For example:

```yaml
- SELECT json_extract(json_result, '$.name') as name, json_extract(json_result, '$.full_name') as full_name FROM json_result WHERE json_extract(json_result, '$.private') = 0
```

This query extracts the 'name' and 'full_name' from JSON data for public repositories.

### XML Queries

For XML data, the system first converts it to JSON, then you can query it. For example:

```yaml
- SELECT xml_to_json(result) as json_result, json_extract(xml_to_json(result), '$.domain.name') as domain_name FROM query WHERE method_name = 'list_domains'
```

This query extracts domain names from XML data stored in the 'result' column.

### Usage

To use these SQL queries:

1. Add them to the `commands.yaml` file under the `commands.python.sentence` section.
2. Run the `runner.py` script, and it will execute these SQL queries along with other commands.

You can create your own custom queries following these patterns to extract and analyze data from JSON or XML results stored in the database.

## Logging

The project now uses a dedicated log file (`.logs`) to store detailed information about the execution process. This includes:

- Information about available modules and methods
- Execution of each command
- Results of command executions
- Any errors or exceptions that occur during the process

The log file provides a comprehensive record of the runner's activities, which can be invaluable for debugging and auditing purposes.

## Usage

To run the command runner:

```
python runner.py
```

Make sure you have the `.env`, `commands.yaml`, and `.private` files in the correct locations as specified in your `.env` file.

## Using Real Credentials

To use the runner with real credentials:

1. Open the `.private` file.
2. Replace the placeholder values with your actual API keys, tokens, and other credentials.
3. In the `commands.yaml` file, use the appropriate account aliases that you've defined in `.private`.
4. Save both files.
5. Run the runner as described in the Usage section.

**IMPORTANT**: Never commit your `.private` file with real credentials to version control. Add it to your `.gitignore` file to prevent accidental commits.

## Starting Projects and Running Tests

To start a new project:

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/command-runner.git
   cd command-runner
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create your `commands.yaml` file based on the provided example.

4. Create your `.private` file and add your actual API keys and tokens.

5. Set up your `.env` file with the correct paths for `.private`, `commands.yaml`, the SQLite database, and the log file.

6. Run the runner:
   ```
   python runner.py
   ```

7. Check the `.logs` file for detailed execution information.

## Running Tests

The project includes a comprehensive suite of unit tests. To run the tests:

1. Make sure you're in the project root directory.

2. Run all tests using the provided bash script:
   ```
   ./run_tests.sh
   ```

3. To run tests for a specific service:
   ```
   ./run_tests.sh <service_name>
   ```
   Replace `<service_name>` with the name of the service (e.g., cloudflare_service, gitlab_service).

4. For more detailed information about testing, refer to the `TESTING.md` file.

## Dependencies

- PyYAML: Used for parsing YAML files.
- Requests: Used for making HTTP requests to APIs.
- python-dotenv: Used for loading environment variables from .env file.
- sqlite3: Used for database operations (part of Python standard library).

## Configuration

1. Modify the `commands.yaml` file to include the commands you want to execute, using appropriate account aliases.
2. Update the `.private` file with your actual credentials for each service and account.
3. Set up the `.env` file with the correct paths for `.private`, `commands.yaml`, the SQLite database, and the log file.

## Extending the Project

This project is designed to be extensible. You can add new service classes by creating new Python files in the `python/` directory. The `runner.py` script will automatically recognize and import these new classes.

To add a new service:

1. Create a new Python file in the `python/` directory (e.g., `new_service.py`).
2. Define your service class with the necessary methods.
3. Add commands using your new service to the `commands.yaml` file.
4. Add the corresponding configuration to the `.private` file.
5. Create unit tests for your new service in the `tests/` directory.

The runner will automatically detect and make available your new service.

## Recent Updates

### Unit Testing

- Added comprehensive unit tests for all services and modules.
- Created a bash script (`run_tests.sh`) to easily run tests.
- Added documentation for running and writing tests in `TESTING.md`.

### SQL Queries on JSON and XML Data

- Added support for executing SQL queries on JSON and XML data stored in the 'result' column.
- Updated `runner.py` to handle JSON and XML queries using SQLite's JSON1 extension.
- Added example queries in `commands.yaml` to demonstrate the new functionality.

### Logging Enhancements

- Added a dedicated log file (`.logs`) to store detailed execution information.
- Updated the `.env` file to include the `LOG_FILE_PATH` variable.
- Modified `runner.py` to use the new logging configuration.

### Database Integration

- Added SQLite database functionality to store command execution results.
- Implemented `runnerdb.py` to handle database operations.
- Updated `runner.py` to use the database for storing and retrieving command results.

### PleskService Improvements

The PleskService class has been updated to address some issues:

1. SSL verification warnings are now suppressed. Note that this is not recommended for production use, and proper SSL verification should be implemented in a real-world scenario.
2. Error handling has been improved in the `create_database` method.
3. Logging has been added throughout the class to help diagnose issues.

### GitHubService Enhancements

The GitHubService class has been updated with the following improvements:

1. A new `list_all_repositories` method has been added to fetch all repositories without filtering.
2. The `list_repositories` method now supports flexible filtering:
   - You can specify a `filter_key` (default is 'name') and a `filter_value`.
   - Filtering is case-insensitive.
   - If no filter is applied, all repositories are returned.
3. Error handling and logging have been added to all methods.
4. A private `_get_repositories` method has been introduced to reduce code duplication.
5. Docstrings have been added to improve documentation.

To use the updated GitHubService methods in your `commands.yaml`:

```yaml
commands:
  python:
    sentence:
      - list all repositories github_main
      - list repositories github_main filter_key=name filter_value=myrepo
      - list repositories github_main  # Lists all repositories (same as list all repositories)
      - create issue github_main repo_owner=owner repo_name=repo title="New Issue" body="This is a test issue"
```

## License

Please refer to the LICENSE file in the project repository for licensing information.
