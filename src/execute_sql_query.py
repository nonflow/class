import sqlite3
import logging
from runnerdb import DB_PATH

logger = logging.getLogger(__name__)

def execute_sql_query(query):
    """Execute a SQL query and return the results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Execute the actual query
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        logger.info(f"SQL query executed: {query}")
        logger.info(f"Number of results: {len(results)}")
        return column_names, results
    except sqlite3.Error as e:
        logger.error(f"SQL error: {e}")
        return None, None
    finally:
        conn.close()
