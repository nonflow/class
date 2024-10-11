import sqlite3
import json
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
QUERY_RESULTS_TABLE = "query"

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

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
