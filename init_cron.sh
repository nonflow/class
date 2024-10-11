#!/bin/bash

# Get the absolute path of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set up the cron job to run eventdb.py every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/python3 $SCRIPT_DIR/eventdb.py >> $SCRIPT_DIR/cron.log 2>&1") | crontab -

echo "Cron job has been set up to run eventdb.py every 5 minutes."
echo "Logs will be written to $SCRIPT_DIR/cron.log"

# Make eventdb.py executable
chmod +x "$SCRIPT_DIR/eventdb.py"

echo "eventdb.py has been made executable."

# Create a virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "Virtual environment created."
fi

# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Install required packages
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "Required packages have been installed in the virtual environment."

# Deactivate the virtual environment
deactivate

echo "Initialization complete. The cron job will use the virtual environment to run eventdb.py."
