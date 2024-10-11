import importlib
import inspect
import yaml
import sys
import shlex
import os
import json
import logging
import sqlite3
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from runnerdb import save_result, get_latest_result, DB_PATH

# Load environment variables from .env file
load_dotenv()

# Configure logging
LOG_FILE = os.getenv('LOG_FILE_PATH', '.logs')
DEBUG_MODE = os.getenv('DEBUG_MODE', '0') == '1'
DEBUG_LEVEL = os.getenv('DEBUG_LEVEL', 'INFO,WARNING,ERROR').split(',')

logging_level = logging.DEBUG if DEBUG_MODE else logging.INFO

logging.basicConfig(
    level=logging_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE,
    filemode='a'
)

# Only add console handler if DEBUG_MODE is True
if DEBUG_MODE:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(console_handler)

logger = logging.getLogger(__name__)

# Add the 'python' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

# Define global variables
PRIVATE_YAML_PATH = os.getenv('PRIVATE_YAML_PATH', 'private.yaml')
COMMANDS_YAML_PATH = os.getenv('COMMANDS_YAML_PATH', 'commands.yaml')

logger.debug(f"PRIVATE_YAML_PATH: {PRIVATE_YAML_PATH}")
logger.debug(f"COMMANDS_YAML_PATH: {COMMANDS_YAML_PATH}")

# Load configuration
commands_data = None
service_config = None
classes_and_objects = None
aliases = None
converters = None

def load_yaml(file_path):
    logger.debug(f"Loading YAML file: {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def list_classes_and_objects():
    logger.debug("Listing classes and objects")
    classes_and_objects = {}
    python_dir = os.path.join(os.path.dirname(__file__), 'python')
    
    for filename in os.listdir(python_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            logger.debug(f"Importing module: {module_name}")
            module = importlib.import_module(module_name)
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    logger.debug(f"Found class: {name}")
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

def filter_data(data, filter_key, filter_value):
    if isinstance(data, list):
        return [item for item in data if str(item.get(filter_key, '')).lower() == str(filter_value).lower()]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if str(v.get(filter_key, '')).lower() == str(filter_value).lower()}
    else:
        return data

def print_value(data, value_key, filter_key, filter_value):
    filtered_data = filter_data(data, filter_key, filter_value)
    if filtered_data:
        if isinstance(filtered_data, list):
            for item in filtered_data:
                print(f"{value_key}: {item.get(value_key, 'Not found')}")
        elif isinstance(filtered_data, dict):
            print(f"{value_key}: {filtered_data.get(value_key, 'Not found')}")
    else:
        print(f"No data found matching the filter: {filter_key}={filter_value}")

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    return json.dumps(xml_to_dict(root))

def xml_to_dict(element):
    result = {}
    for child in element:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(child)
    return result

def create_json_result_view():
    """Create the json_result view if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TEMP VIEW IF NOT EXISTS json_result AS SELECT id, result FROM query")
        conn.commit()
        logger.info("Created json_result view")
    except sqlite3.Error as e:
        logger.error(f"Error creating json_result view: {e}")
    finally:
        conn.close()

def execute_sql_query(query):
    """Execute a SQL query and return the results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Execute the actual query
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        logger.info(f"SQL query executed: {query}")
        logger.info(f"Number of results: {len(results)}")
        return column_names, results
    except sqlite3.Error as e:
        logger.error(f"SQL error: {e}")
        return None, None
    finally:
        conn.close()

def execute_command(command, classes_and_objects, service_config):
    logger.info(f"Executing command: {command}")
    
    # Check if the command is a SQL query
    if command.strip().upper().startswith("SELECT"):
        column_names, results = execute_sql_query(command)
        if column_names and results:
            # Print column names
            print(" | ".join(column_names))
            print("-" * (sum(len(name) for name in column_names) + 3 * (len(column_names) - 1)))
            # Print results
            for row in results:
                print(" | ".join(str(value) for value in row))
            logger.info(f"SQL query results printed")
        else:
            logger.warning("No results returned from SQL query")
        return

    parts = shlex.split(command)
    if len(parts) < 2:
        logger.error(f"Invalid command format: {command}")
        return

    action = parts[0].lower()
    if action == 'filter':
        # Handle filter command
        data_key = parts[1]
        filter_key = parts[2]
        filter_value = parts[3]
        service_name, method_name = data_key.split('_', 1)
        data = get_latest_result(service_name, method_name)
        if data:
            filtered_data = filter_data(data, filter_key, filter_value)
            save_result(command, 'name', service_name, method_name, filtered_data)
            logger.info(f"Filtered data saved for '{data_key}'")
        else:
            logger.error(f"No data found with key '{data_key}'")
        return
    elif action == 'print' and parts[1] == 'value':
        # Handle print value command
        value_key = parts[2]
        filter_key, filter_value = parts[4].split('=')
        service_name, method_name = parts[-1].split('_', 1)
        data = get_latest_result(service_name, method_name)
        if data:
            print_value(data, value_key, filter_key, filter_value)
            logger.info(f"Printed value for {service_name}.{method_name}")
        else:
            logger.error(f"No data found for {service_name}_{method_name}")
        return

    method_parts = []
    account_alias = None
    for part in parts:
        if part in service_config:
            account_alias = part
            break
        method_parts.append(part)

    if not account_alias:
        logger.error(f"Invalid account alias in command: {command}")
        return

    method_name = '_'.join(method_parts).lower()
    service_info = service_config[account_alias]

    service_name = service_info['service']

    if service_name not in classes_and_objects:
        logger.error(f"Invalid service name: {service_name}")
        return

    service_class = classes_and_objects[service_name]['class']
    constructor_args = {k: v for k, v in service_info.items() if k != 'service'}

    # Create an instance of the service
    try:
        instance = service_class(**constructor_args)
    except TypeError as e:
        logger.error(f"Error creating {service_name} instance: {str(e)}")
        return

    if method_name not in classes_and_objects[service_name]['methods']:
        logger.error(f"Method {method_name} not found in class {service_name}.")
        return

    method = classes_and_objects[service_name]['methods'][method_name]

    # Parse method arguments
    method_args = parse_command_args(parts[len(method_parts)+1:])

    try:
        result = method(instance, **method_args)
        logger.info(f"Result of {service_name}.{method_name}: {result}")
        
        # Save the result to the database
        save_result(command, account_alias, service_name, method_name, result)
        logger.info(f"Data saved for {service_name}.{method_name}")
    except Exception as e:
        logger.error(f"Error executing {service_name}.{method_name}: {str(e)}")

def main():
    global commands_data, service_config, classes_and_objects, aliases, converters

    commands_data = load_yaml(COMMANDS_YAML_PATH)
    service_config = load_yaml(PRIVATE_YAML_PATH)

    logger.debug(f"Service config: {service_config}")

    classes_and_objects = list_classes_and_objects()

    logger.info("Available modules and methods:")
    for class_name, class_info in classes_and_objects.items():
        logger.info(f"\nClass: {class_name}")
        logger.info("  Methods:")
        for method_name, method_obj in class_info['methods'].items():
            logger.info(f"    - {method_name}")
            logger.info(f"      {inspect.signature(method_obj)}")

    aliases = commands_data['commands']['python'].get('alias', {})
    converters = commands_data['commands']['python'].get('convert', {}).get('param', {})
    
    # Create json_result view
    create_json_result_view()
    
    logger.info("\nExecuting commands:")
    for command in commands_data['commands']['python']['sentence']:
        replaced_command = replace_aliases(command, aliases, converters)
        logger.info(f"\nRUN: {command}")
        if replaced_command != command:
            logger.info(f"Replaced: {replaced_command}")
        execute_command(replaced_command, classes_and_objects, service_config)

if __name__ == "__main__":
    main()
