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

This project implements a flexible command runner system that dynamically loads and executes commands from a YAML file. It includes functionality for interacting with various services such as Cloudflare, GitLab, GitHub, and Plesk.

## Project Structure

The project consists of the following main components:

1. `runner.py`: The main script that loads commands from a YAML file and executes them.
2. `python/`: Directory containing service classes (e.g., CloudflareService, GitLabService, GitHubService, PleskService).
3. `commands.yaml`: Contains the list of commands to be executed by the runner.
4. `.private`: Stores sensitive information like API keys and tokens.
5. `.env`: Contains environment variables for configuring file paths.
6. `requirements.txt`: Lists the Python dependencies for the project.
7. `logo/`: Directory containing logo files for the project.

## How It Works

1. The `runner.py` script is the entry point of the application. It does the following:
   - Loads environment variables from the `.env` file.
   - Loads commands from the specified YAML file.
   - Loads service configuration from `.private`.
   - Dynamically imports and recognizes all service classes in the `python/` directory.
   - Lists available classes and their methods.
   - Executes the commands specified in the YAML file.

2. Each service class provides methods for interacting with their respective APIs.

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

The `.env` file is used to set the paths for the `.private` and `commands.yaml` files. It has the following structure:

```
PRIVATE_YAML_PATH=.private
COMMANDS_YAML_PATH=commands.yaml
```

This allows you to easily change the location of these files without modifying the `runner.py` script.

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

5. Set up your `.env` file with the correct paths for `.private` and `commands.yaml`.

6. Run the runner:
   ```
   python runner.py
   ```

## Dependencies

- PyYAML: Used for parsing YAML files.
- Requests: Used for making HTTP requests to APIs.
- python-dotenv: Used for loading environment variables from .env file.

## Configuration

1. Modify the `commands.yaml` file to include the commands you want to execute, using appropriate account aliases.
2. Update the `.private` file with your actual credentials for each service and account.
3. Set up the `.env` file with the correct paths for `.private` and `commands.yaml`.

## Extending the Project

This project is designed to be extensible. You can add new service classes by creating new Python files in the `python/` directory. The `runner.py` script will automatically recognize and import these new classes.

To add a new service:

1. Create a new Python file in the `python/` directory (e.g., `new_service.py`).
2. Define your service class with the necessary methods.
3. Add commands using your new service to the `commands.yaml` file.
4. Add the corresponding configuration to the `.private` file.

The runner will automatically detect and make available your new service.

## Recent Updates

### PleskService Improvements

The PleskService class has been updated to address some issues:

1. SSL verification warnings are now suppressed. Note that this is not recommended for production use, and proper SSL verification should be implemented in a real-world scenario.
2. Error handling has been improved in the `create_database` method.
3. Logging has been added throughout the class to help diagnose issues.

### GitHubService Enhancements

The GitHubService class has been updated with the following improvements:

1. The `list_repositories` method now supports more flexible filtering:
   - You can specify a `filter_key` (default is 'name') and a `filter_value`.
   - Filtering is case-insensitive.
   - If no filter is applied, all repositories are returned.
2. Error handling and logging have been added to both `list_repositories` and `create_issue` methods.
3. Docstrings have been added to improve documentation.

To use the updated `list_repositories` method in your `commands.yaml`:

```yaml
commands:
  python:
    sentence:
      - list repositories github_main filter_key=name filter_value=myrepo
      - list repositories github_main  # Lists all repositories
```

### Logging

Logging has been implemented in both PleskService and GitHubService classes. To view more detailed logs, you can adjust the logging level in your Python script or environment. For example:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show more detailed log messages, which can be helpful for troubleshooting.

## License

Please refer to the LICENSE file in the project repository for licensing information.
