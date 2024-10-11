import importlib
import inspect
import yaml
import sys
import shlex
import os

# Add the 'python' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def list_classes_and_objects():
    modules = ['Account', 'Message']
    classes_and_objects = {}

    for module_name in modules:
        module = importlib.import_module(module_name)
        classes_and_objects[module_name] = {
            'class': None,
            'methods': {}
        }

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name == module_name:
                classes_and_objects[module_name]['class'] = obj
                for method_name, method_obj in inspect.getmembers(obj):
                    if inspect.isfunction(method_obj) or inspect.ismethod(method_obj):
                        classes_and_objects[module_name]['methods'][method_name] = method_obj

    return classes_and_objects

def replace_aliases(command, aliases):
    parts = shlex.split(command)
    new_parts = []
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            new_key = aliases['param'].get(key, key)
            new_value = aliases['modifier'].get(value, value)
            new_parts.append(f"{new_key}={new_value}")
        else:
            new_parts.append(aliases['action'].get(part, part))
    return ' '.join(new_parts)

def execute_command(command, classes_and_objects):
    parts = shlex.split(command)
    if len(parts) < 2:
        print(f"Error: Invalid command format: {command}")
        return

    module_name, method_name = parts[0], parts[1]
    if module_name not in classes_and_objects:
        print(f"Error: Module {module_name} not found.")
        return

    class_obj = classes_and_objects[module_name]['class']
    if not class_obj:
        print(f"Error: Class not found in module {module_name}.")
        return

    instance = class_obj()

    if not hasattr(instance, method_name):
        print(f"Error: Method {method_name} not found in class {module_name}.")
        return

    method = getattr(instance, method_name)
    method_args = {}
    for arg in parts[2:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            method_args[key] = value
        else:
            method_args[arg] = True

    try:
        result = method(**method_args)
        print(f"Result of {module_name}.{method_name}: {result}")
    except Exception as e:
        print(f"Error executing {module_name}.{method_name}: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python runner.py commands.yaml")
        sys.exit(1)

    commands_file = sys.argv[1]
    commands_data = load_yaml(commands_file)

    classes_and_objects = list_classes_and_objects()

    print(classes_and_objects)
    print("Available modules and methods:")
    for module_name, module_info in classes_and_objects.items():
        print(f"\nModule: {module_name}")
        print("  Class:", module_info['class'].__name__ if module_info['class'] else "Not found")
        print("  Methods:")
        for method_name, method_obj in module_info['methods'].items():
            print(f"    - {method_name}")
            print(f"      {inspect.signature(method_obj)}")

    aliases = commands_data['commands']['python']['alias']
    print("\nExecuting commands:")
    for command in commands_data['commands']['python']:
        if isinstance(command, str):  # Skip the 'alias' dictionary
            replaced_command = replace_aliases(command, aliases)
            print(f"\nRUN: {command}")
            print(f"Replaced: {replaced_command}")
            execute_command(replaced_command, classes_and_objects)

if __name__ == "__main__":
    main()
