import requests
import xml.etree.ElementTree as ET

class PleskService:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"https://{host}:8443/enterprise/control/agent.php"

    def _send_request(self, xml_request):
        headers = {
            "Content-Type": "text/xml",
            "HTTP_PRETTY_PRINT": "TRUE",
        }
        response = requests.post(
            self.base_url,
            headers=headers,
            auth=(self.username, self.password),
            data=xml_request,
            verify=False  # Note: In production, you should use proper SSL verification
        )
        return ET.fromstring(response.content)

    def list_domains(self):
        xml_request = """
        <packet>
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
        domains = []
        for domain in response.findall(".//name"):
            domains.append(domain.text)
        return domains

    def create_database(self, webspace_name, db_name, db_user, db_password):
        xml_request = f"""
        <packet>
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
        return "Database created successfully" if response.find(".//result").get("code") == "ok" else "Failed to create database"
