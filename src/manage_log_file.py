import os
from datetime import datetime

def manage_log_file(LOG_FILE, REMOVE_LOGS_AFTER):
    if REMOVE_LOGS_AFTER == 1:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        print(f"Log file {LOG_FILE} has been removed.")
    elif REMOVE_LOGS_AFTER > 1:
        if os.path.exists(LOG_FILE):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
            if file_age.days >= REMOVE_LOGS_AFTER:
                os.remove(LOG_FILE)
                print(f"Log file {LOG_FILE} has been removed as it was older than {REMOVE_LOGS_AFTER} days.")
