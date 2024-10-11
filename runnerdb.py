import sqlite3
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
QUERY_RESULTS_TABLE = "query"

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

def init_db():
    """Initialize the database and create the necessary table if it doesn't exist."""
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
    conn.commit()
    conn.close()
    logger.debug("Database initialized")

def save_result(command, name, service_name, method_name, result):
    """Save the result of a query to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert result to JSON string if it's not already a string
    if not isinstance(result, str):
        result = json.dumps(result)
    
    cursor.execute(f'''
    INSERT INTO {QUERY_RESULTS_TABLE} (command, name, service_name, method_name, result)
    VALUES (?, ?, ?, ?, ?)
    ''', (command, name, service_name, method_name, result))
    
    conn.commit()
    conn.close()
    logger.debug(f"Result saved for {service_name}.{method_name}")

def get_latest_result(service_name, method_name):
    """Retrieve the latest result for a given service and method."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f'''
    SELECT result FROM {QUERY_RESULTS_TABLE}
    WHERE service_name = ? AND method_name = ?
    ORDER BY timestamp DESC
    LIMIT 1
    ''', (service_name, method_name))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        try:
            return json.loads(result[0])
        except json.JSONDecodeError:
            return result[0]
    logger.debug(f"Retrieved latest result for {service_name}.{method_name}")
    return None

# Initialize the database when this module is imported
init_db()
