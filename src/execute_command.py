import logging
import shlex
from src.execute_sql_query import execute_sql_query
from src.filter_data import filter_data
from src.print_value import print_value
from src.parse_command_args import parse_command_args
from runnerdb import save_result, get_latest_result

logger = logging.getLogger(__name__)

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
