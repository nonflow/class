import sqlite3
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
SCHEDULED_TASKS_TABLE = "scheduled_tasks"

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

def update_scheduled_task(task_id, last_run, next_run, status):
    """Update the status of a scheduled task."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
    UPDATE {SCHEDULED_TASKS_TABLE}
    SET last_run = ?, next_run = ?, status = ?
    WHERE id = ?
    ''', (last_run, next_run, status, task_id))
    
    conn.commit()
    conn.close()
    logger.debug(f"Updated scheduled task {task_id}")
