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
