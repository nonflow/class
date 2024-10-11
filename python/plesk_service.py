import requests
import json
import warnings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress only the single InsecureRequestWarning
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class PleskService:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"https://{host}:8443/api/v2"
        self.api_key = self.generate_plesk_api_key()

    def generate_plesk_api_key(self):
        url = f"{self.base_url}/auth/keys"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {}  # Empty JSON object as per the API documentation

        try:
            response = requests.post(
                url,
                auth=(self.username, self.password),
                headers=headers,
                json=data,
                verify=False  # Note: In production, you should verify SSL certificates
            )
            response.raise_for_status()
            api_key = response.json().get('key')
            if api_key:
                logger.info("API key generated successfully")
                return api_key
            else:
                logger.error("API key not found in the response")
                return None
        except requests.RequestException as e:
            logger.error(f"Error generating API key: {e}")
            return None

    def _send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Key': self.api_key
        }

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                verify=False  # Note: In production, you should use proper SSL verification
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error sending request to Plesk: {e}")
            return None

    def list_domains(self):
        logger.info("Fetching list of domains from Plesk")
        response = self._send_request('GET', 'domains')
        if response is None:
            logger.error("Failed to get response from Plesk server")
            return []

        domains = [domain['name'] for domain in response]

        if not domains:
            logger.info("No domains found in Plesk account")
        else:
            logger.info(f"Found {len(domains)} domains")

        return domains

    def create_database(self, webspace_name, db_name, db_user, db_password):
        logger.info(f"Creating database {db_name} in webspace {webspace_name}")
        data = {
            "webspace": webspace_name,
            "name": db_name,
            "type": "mysql",
            "server": "localhost",
            "user": {
                "name": db_user,
                "password": db_password
            }
        }
        response = self._send_request('POST', 'databases', data)
        if response is None:
            return "Failed to create database: No response from server"

        if 'id' in response:
            logger.info(f"Database {db_name} created successfully")
            return "Database created successfully"
        else:
            error_message = response.get('message', 'Unknown error')
            logger.error(f"Failed to create database: {error_message}")
            return f"Failed to create database: {error_message}"


