import sqlite3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

def init_db():
    """Initialize the database and create the necessary table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS query_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT,
        method_name TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def save_result(service_name, method_name, result):
    """Save the result of a query to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert result to JSON string if it's not already a string
    if not isinstance(result, str):
        result = json.dumps(result)
    
    cursor.execute('''
    INSERT INTO query_results (service_name, method_name, result)
    VALUES (?, ?, ?)
    ''', (service_name, method_name, result))
    
    conn.commit()
    conn.close()

def get_latest_result(service_name, method_name):
    """Retrieve the latest result for a given service and method."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT result FROM query_results
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
    return None

# Initialize the database when this module is imported
init_db()
