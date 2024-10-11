import os
import sys
import logging
from datetime import datetime, timedelta
from croniter import croniter
from dotenv import load_dotenv

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runnerdb import get_scheduled_tasks, update_scheduled_task
from runner import execute_command, load_yaml, list_classes_and_objects

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_scheduled_tasks():
    tasks = get_scheduled_tasks()
    now = datetime.now()

    # Load configuration
    commands_data = load_yaml(os.getenv('COMMANDS_YAML_PATH', 'commands.yaml'))
    service_config = load_yaml(os.getenv('PRIVATE_YAML_PATH', 'private.yaml'))
    classes_and_objects = list_classes_and_objects()

    for task in tasks:
        task_id, command, schedule, last_run, next_run, status = task

        if next_run is None or now >= datetime.fromisoformat(next_run):
            logger.info(f"Running task {task_id}: {command}")

            try:
                execute_command(command, classes_and_objects, service_config)
                status = 'completed'
            except Exception as e:
                logger.error(f"Error executing task {task_id}: {str(e)}")
                status = 'failed'

            last_run = now.isoformat()
            cron = croniter(schedule, now)
            next_run = cron.get_next(datetime).isoformat()

            update_scheduled_task(task_id, last_run, next_run, status)
            logger.info(f"Task {task_id} completed. Next run: {next_run}")

if __name__ == "__main__":
    run_scheduled_tasks()
