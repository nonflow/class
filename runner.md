# runner.py Documentation

## Overview
`runner.py` is a Python script that serves as a command runner for the project. It dynamically loads classes and methods from specified modules, and executes commands based on a YAML configuration file.

## Usage
To use this script, run the following command:

```
python runner.py commands.yaml
```

Where `commands.yaml` is the YAML file containing the commands to be executed.

## Main Components

1. `load_yaml(file_path)`: 
   - Loads and returns the content of a YAML file.

2. `list_classes_and_objects()`:
   - Dynamically imports the 'Account' and 'Message' modules.
   - Collects classes and their methods from these modules.
   - Returns a dictionary with module names as keys, containing class objects and their methods.

3. `execute_command(command, classes_and_objects)`:
   - Parses and executes a given command string.
   - Dynamically calls the specified method of the specified class with given arguments.
   - Prints the result or any errors encountered during execution.

4. `main()`:
   - Entry point of the script.
   - Loads commands from the YAML file specified as a command-line argument.
   - Lists available modules, classes, and methods.
   - Executes each command from the YAML file.

## Script Flow
1. The script starts by checking if a YAML file is provided as a command-line argument.
2. It then loads the commands from the YAML file.
3. Classes and objects from 'Account' and 'Message' modules are dynamically loaded.
4. Available modules, classes, and methods are printed for reference.
5. Each command from the YAML file is executed using the `execute_command` function.

## Notes
- The script assumes the existence of 'Account' and 'Message' modules in the same directory or in the Python path.
- Commands in the YAML file should follow the format: `ModuleName MethodName [arg1=value1 arg2=value2 ...]`
- Error handling is implemented to catch and display issues with command execution.
- The script uses dynamic importing and reflection to load and execute methods, providing flexibility in command execution.

## Dependencies
- PyYAML: For parsing the YAML configuration file.
- importlib: For dynamic module importing.
- inspect: For introspection of classes and methods.
- sys: For accessing command-line arguments.
- shlex: For parsing command strings.

Ensure all dependencies are installed before running the script.
