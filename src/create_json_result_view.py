import sqlite3
import logging
from runnerdb import DB_PATH

logger = logging.getLogger(__name__)

def create_json_result_view():
    """Create the json_result view if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TEMP VIEW IF NOT EXISTS json_result AS SELECT id, result FROM query")
        conn.commit()
        logger.info("Created json_result view")
    except sqlite3.Error as e:
        logger.error(f"Error creating json_result view: {e}")
    finally:
        conn.close()
