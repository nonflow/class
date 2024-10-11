import logging
from runnerdb import add_scheduled_task

logger = logging.getLogger(__name__)

def process_scheduled_tasks(scheduled_tasks):
    logger.info("Processing scheduled tasks")
    for task in scheduled_tasks:
        command = task['command']
        schedule = task['cron']
        logger.info(f"Adding scheduled task: {command} with schedule: {schedule}")
        add_scheduled_task(command, schedule)
