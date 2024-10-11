import yaml
import logging

logger = logging.getLogger(__name__)

def load_yaml(file_path):
    logger.debug(f"Loading YAML file: {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
