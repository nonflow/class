import importlib
import inspect
import yaml
import sys
import shlex
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the 'python' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# Define global variables
PRIVATE_YAML_PATH = os.getenv('PRIVATE_YAML_PATH', 'private.yaml')
COMMANDS_YAML_PATH = os.getenv('COMMANDS_YAML_PATH', 'commands.yaml')

# Load configuration
commands_data = None
service_config = None
classes_and_objects = None
aliases = None
converters = None

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def list_classes_and_objects():
    classes_and_objects = {}
    python_dir = os.path.join(os.path.dirname(__file__), 'python')
    
    for filename in os.listdir(python_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = importlib.import_module(module_name)
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    classes_and_objects[name] = {
                        'class': obj,
                        'methods': {method_name.lower(): method_obj for method_name, method_obj in inspect.getmembers(obj) if inspect.isfunction(method_obj) or inspect.ismethod(method_obj)}
                    }

    return classes_and_objects

def get_function_from_string(func_string):
    module_name, func_name = func_string.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)

def replace_aliases(command, aliases, converters):
    parts = shlex.split(command)
    new_parts = []
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            new_key = aliases.get('param', {}).get(key, key)  # Use original if no alias
            new_value = value  # Start with the original value
            
            # Apply converter if available
            if value in converters:
                converter_func = get_function_from_string(converters[value])
                if converter_func:
                    new_value = converter_func()
            
            new_parts.append(f"{new_key}={new_value}")
        else:
            # Use original if 'action' key doesn't exist or if there's no alias for this action
            new_parts.append(aliases.get('action', {}).get(part.lower(), part))
    return ' '.join(new_parts)

def parse_command_args(args):
    parsed_args = {}
    key = None
    value = []
    in_quotes = False

    for arg in args:
        if '=' in arg and not in_quotes:
            if key:
                parsed_args[key] = ' '.join(value)
            key, val = arg.split('=', 1)
            value = [val]
            in_quotes = val.startswith('"') and not val.endswith('"')
        elif in_quotes:
            value.append(arg)
            if arg.endswith('"'):
                in_quotes = False
        elif key:
            value.append(arg)
        else:
            parsed_args[arg] = True

    if key:
        parsed_args[key] = ' '.join(value)

    # Remove quotes from values
    for k, v in parsed_args.items():
        if isinstance(v, str):
            parsed_args[k] = v.strip('"')

    return parsed_args

def execute_command(command, classes_and_objects, service_config):
    parts = shlex.split(command)
    if len(parts) < 2:
        print(f"Error: Invalid command format: {command}")
        return

    method_parts = []
    account_alias = None
    for part in parts:
        if part in service_config:
            account_alias = part
            break
        method_parts.append(part)

    if not account_alias:
        print(f"Error: Invalid account alias in command: {command}")
        return

    method_name = '_'.join(method_parts).lower()
    service_info = service_config[account_alias]
    service_name = service_info['service']

    if service_name not in classes_and_objects:
        print(f"Error: Invalid service name: {service_name}")
        return

    service_class = classes_and_objects[service_name]['class']
    constructor_args = {k: v for k, v in service_info.items() if k != 'service'}

    # Create an instance of the service
    try:
        instance = service_class(**constructor_args)
    except TypeError as e:
        print(f"Error creating {service_name} instance: {str(e)}")
        return

    if method_name not in classes_and_objects[service_name]['methods']:
        print(f"Error: Method {method_name} not found in class {service_name}.")
        return

    method = classes_and_objects[service_name]['methods'][method_name]

    # Parse method arguments
    method_args = parse_command_args(parts[len(method_parts)+1:])

    try:
        result = method(instance, **method_args)
        print(f"Result of {service_name}.{method_name}: {result}")
    except Exception as e:
        print(f"Error executing {service_name}.{method_name}: {str(e)}")

def main():
    global commands_data, service_config, classes_and_objects, aliases, converters

    commands_data = load_yaml(COMMANDS_YAML_PATH)
    service_config = load_yaml(PRIVATE_YAML_PATH)

    classes_and_objects = list_classes_and_objects()

    print("Available modules and methods:")
    for class_name, class_info in classes_and_objects.items():
        print(f"\nClass: {class_name}")
        print("  Methods:")
        for method_name, method_obj in class_info['methods'].items():
            print(f"    - {method_name}")
            print(f"      {inspect.signature(method_obj)}")

    aliases = commands_data['commands']['python'].get('alias', {})
    converters = commands_data['commands']['python'].get('convert', {}).get('param', {})
    
    print("\nExecuting commands:")
    for command in commands_data['commands']['python']['sentence']:
        replaced_command = replace_aliases(command, aliases, converters)
        print(f"\nRUN: {command}")
        if replaced_command != command:
            print(f"Replaced: {replaced_command}")
        execute_command(replaced_command, classes_and_objects, service_config)

if __name__ == "__main__":
    main()
