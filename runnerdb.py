import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
QUERY_RESULTS_TABLE = "query"
SCHEDULED_TASKS_TABLE = "scheduled_tasks"

# Get the database path from the environment variable
DB_PATH = os.getenv('SQLITE_DB_PATH', 'runner.db')

from src.init_db import init_db
from src.save_result import save_result
from src.get_latest_result import get_latest_result
from src.add_scheduled_task import add_scheduled_task
from src.get_scheduled_tasks import get_scheduled_tasks
from src.update_scheduled_task import update_scheduled_task

# Initialize the database when this module is imported
init_db()
