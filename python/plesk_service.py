import requests
import xml.etree.ElementTree as ET
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
        self.base_url = f"https://{host}:8443/enterprise/control/agent.php"

    def _create_auth_xml(self):
        return f"""
        <auth>
            <login>{self.username}</login>
            <password>{self.password}</password>
        </auth>
        """

    def _send_request(self, xml_request):
        headers = {
            "Content-Type": "text/xml",
            "HTTP_PRETTY_PRINT": "TRUE",
        }
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=xml_request,
                verify=False  # Note: In production, you should use proper SSL verification
            )
            response.raise_for_status()
            logger.debug(f"XML Response: {response.content.decode('utf-8')}")
            return ET.fromstring(response.content)
        except requests.RequestException as e:
            logger.error(f"Error sending request to Plesk: {e}")
            return None

    def list_domains(self):
        logger.info("Fetching list of domains from Plesk")
        xml_request = f"""
        <packet>
            {self._create_auth_xml()}
            <webspace>
                <get>
                    <filter/>
                    <dataset>
                        <gen_info/>
                    </dataset>
                </get>
            </webspace>
        </packet>
        """
        response = self._send_request(xml_request)
        if response is None:
            logger.error("Failed to get response from Plesk server")
            return []
        
        domains = []
        for domain in response.findall(".//name"):
            domains.append(domain.text)
        
        if not domains:
            logger.info("No domains found in Plesk account")
        else:
            logger.info(f"Found {len(domains)} domains")
        
        return domains

    def create_database(self, webspace_name, db_name, db_user, db_password):
        logger.info(f"Creating database {db_name} in webspace {webspace_name}")
        xml_request = f"""
        <packet>
            {self._create_auth_xml()}
            <database>
                <add>
                    <webspace-id>{webspace_name}</webspace-id>
                    <name>{db_name}</name>
                    <type>mysql</type>
                    <db-server-id>localhost</db-server-id>
                    <user>
                        <name>{db_user}</name>
                        <password>{db_password}</password>
                    </user>
                </add>
            </database>
        </packet>
        """
        response = self._send_request(xml_request)
        if response is None:
            return "Failed to create database: No response from server"
        
        result = response.find(".//result")
        if result is None:
            logger.error(f"Unexpected response structure: {ET.tostring(response, encoding='unicode')}")
            return "Failed to create database: Unexpected response structure"
        
        if result.get("code") == "ok":
            logger.info(f"Database {db_name} created successfully")
            return "Database created successfully"
        else:
            error_text = result.find(".//text")
            error_message = error_text.text if error_text is not None else "Unknown error"
            logger.error(f"Failed to create database: {error_message}")
            return f"Failed to create database: {error_message}"
