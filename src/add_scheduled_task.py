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

def add_scheduled_task(command, schedule):
    """Add a new scheduled task to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
    INSERT INTO {SCHEDULED_TASKS_TABLE} (command, schedule, status)
    VALUES (?, ?, ?)
    ''', (command, schedule, 'pending'))
    
    conn.commit()
    conn.close()
    logger.debug(f"Added new scheduled task: {command}")
