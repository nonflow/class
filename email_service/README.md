# Email Service

This project contains a set of Python classes and utilities for handling email operations.

## Project Structure

```
email_service/
├── src/
│   └── email_service/
│       ├── __init__.py
│       ├── config.py
│       ├── email_ports.json
│       ├── email_reader.py
│       ├── email_sender.py
│       ├── email_service.py
│       └── email_utils.py
├── tests/
│   └── test_email_utils.py
├── README.md
├── requirements.txt
└── setup.py
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/email_service.git
   ```

2. Change to the project directory:
   ```
   cd email_service
   ```

3. Install the package:
   ```
   pip install .
   ```

## Usage

Import the necessary classes from the respective files to use in your project. For example:

```python
from email_service.email_service import EmailService
from email_service.config import config

# Initialize the email service
email_service = EmailService()

# Use the service methods for reading or sending emails
```

## Running Tests

To run the unit tests, use the following command from the project root directory:

```
python -m unittest discover tests
```

## Configuration

The `email_ports.json` file is used for configuring email ports. It is loaded automatically by the `Config` class in `config.py`.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
