import sqlite3
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
QUERY_RESULTS_TABLE = "query"
SCHEDULED_TASKS_TABLE = "scheduled_tasks"

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

def init_db():
    """Initialize the database and create the necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {QUERY_RESULTS_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT,
        name TEXT,
        service_name TEXT,
        method_name TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {SCHEDULED_TASKS_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT,
        schedule TEXT,
        last_run DATETIME,
        next_run DATETIME,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()
    logger.debug("Database initialized")

# Initialize the database when this module is imported
init_db()
