# init.sh Documentation

## Overview
`init.sh` is a Bash script designed to set up the project environment. It automates the process of creating a virtual environment, installing dependencies, and setting up necessary permissions.

## Usage
To use this script, run the following command in the project root directory:

```
./init.sh
```

## Script Components

1. Set execute permissions:
   ```bash
   chmod +x *.sh
   ```
   This line sets execute permissions for all .sh files in the current directory.

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
   This creates a new Python virtual environment named 'venv' in the current directory.

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
   This activates the newly created virtual environment.

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This installs all the Python packages listed in the requirements.txt file.

5. Print success message:
   ```bash
   echo "Project environment set up successfully!"
   echo "To activate the virtual environment, run: source venv/bin/activate"
   ```
   These lines print a success message and provide instructions for activating the virtual environment in the future.

## Notes
- Ensure you have Python 3 and pip installed on your system before running this script.
- The script assumes that there's a `requirements.txt` file in the same directory, listing all the Python dependencies for the project.
- After running the script, you need to activate the virtual environment in new terminal sessions using the command provided in the success message.
