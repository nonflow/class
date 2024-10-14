import json
import logging
import socket
import re
from dateutil import parser

logger = logging.getLogger(__name__)

def load_email_ports():
    try:
        with open('python/email_ports.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load email_ports.json: {str(e)}")
        return {}

def parse_date(date_string):
    """
    Parse a date string in various formats and return it in 'DD-MMM-YYYY' format.
    
    :param date_string: A string representing a date
    :return: A string representing the date in 'DD-MMM-YYYY' format
    """
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime('%d-%b-%Y')
    except ValueError:
        logger.error(f"Unable to parse date: {date_string}")
        return None

def check_ports(host, ports):
    results = {}
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=2) as sock:
                results[port] = "Open"
        except socket.error as e:
            if e.errno == 111:  # Connection refused
                results[port] = "Connection refused"
            else:
                results[port] = f"Error: {e}"
    return results

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
