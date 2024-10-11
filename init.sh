#!/bin/bash

chmod +x *.sh

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Print success message
echo "Project environment set up successfully!"
echo "To activate the virtual environment, run: source venv/bin/activate"
