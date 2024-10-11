```bash
_   _             _____ _               
| \ | |           |  ___| |              
|  \| | ___  _ __ | |_  | | _____      __
| . ` |/ _ \| '_ \|  _| | |/ _ \ \ /\ / /
| |\  | (_) | | | | |   | | (_) \ V  V / 
\_| \_/\___/|_| |_\_|   |_|\___/ \_/\_/  
```

# Run Command by Sentences
![NonFlow Logo](logo/nonflow.svg)

This project implements a flexible command runner system that dynamically loads and executes commands from a YAML file. It includes functionality for interacting with various services such as Cloudflare, GitLab, GitHub, and Plesk.

## Project Structure

The project consists of the following main components:

1. `runner.py`: The main script that loads commands from a YAML file and executes them.
2. `python/`: Directory containing service classes (e.g., CloudflareService, GitLabService, GitHubService, PleskService).
3. `commands.yaml`: Contains the list of commands to be executed by the runner.
4. `requirements.txt`: Lists the Python dependencies for the project.
5. `logo/`: Directory containing logo files for the project.

## How It Works

1. The `runner.py` script is the entry point of the application. It does the following:
   - Loads commands from the specified YAML file.
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
      - list zones CloudflareService api_key=your_api_key email=your_email@example.com
      - list projects GitLabService base_url=https://gitlab.com private_token=your_private_token
      # ... more commands ...
```

Each command specifies the method to call (using spaces instead of underscores), the service to use, and the necessary parameters.

## Usage

To run the command runner:

```
python runner.py commands.yaml
```

Make sure you have a `commands.yaml` file in the same directory with the list of commands you want to execute.

## Using Real Credentials

To use the runner with real credentials:

1. Open the `commands.yaml` file.
2. Replace the placeholder values with your actual API keys, tokens, and other credentials. For example:
   ```yaml
   - list zones CloudflareService api_key=your_actual_api_key email=your_actual_email@example.com
   ```
3. Save the `commands.yaml` file.
4. Run the runner as described in the Usage section.

**IMPORTANT**: Never commit your real credentials to version control. Consider using environment variables or a separate, gitignored configuration file for sensitive information.

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

4. Replace the placeholder credentials in `commands.yaml` with your actual API keys and tokens.

5. Run the runner:
   ```
   python runner.py commands.yaml
   ```

## Dependencies

- PyYAML: Used for parsing YAML files.
- Requests: Used for making HTTP requests to APIs.

## Configuration

Modify the `commands.yaml` file to include the commands you want to execute with the appropriate credentials.

## Extending the Project

This project is designed to be extensible. You can add new service classes by creating new Python files in the `python/` directory. The `runner.py` script will automatically recognize and import these new classes.

To add a new service:

1. Create a new Python file in the `python/` directory (e.g., `new_service.py`).
2. Define your service class with the necessary methods.
3. Add commands using your new service to the `commands.yaml` file.

The runner will automatically detect and make available your new service.

## License

Please refer to the LICENSE file in the project repository for licensing information.
