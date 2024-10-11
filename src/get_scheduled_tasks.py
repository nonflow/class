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

def get_scheduled_tasks():
    """Retrieve all scheduled tasks from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
    SELECT id, command, schedule, last_run, next_run, status
    FROM {SCHEDULED_TASKS_TABLE}
    ''')
    
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks
