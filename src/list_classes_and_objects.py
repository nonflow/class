import os
import importlib
import inspect
import logging

logger = logging.getLogger(__name__)

def list_classes_and_objects():
    logger.debug("Listing classes and objects")
    classes_and_objects = {}
    python_dir = os.path.join(os.path.dirname(__file__), '..', 'python')
    
    for filename in os.listdir(python_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            logger.debug(f"Importing module: {module_name}")
            module = importlib.import_module(f"python.{module_name}")
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == f"python.{module_name}":
                    logger.debug(f"Found class: {name}")
                    classes_and_objects[name] = {
                        'class': obj,
                        'methods': {method_name.lower(): method_obj for method_name, method_obj in inspect.getmembers(obj) if inspect.isfunction(method_obj) or inspect.ismethod(method_obj)}
                    }

    return classes_and_objects
