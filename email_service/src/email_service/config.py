import os
import json

class Config:
    def __init__(self):
        self.email_ports = self.load_email_ports()

    def load_email_ports(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        email_ports_path = os.path.join(current_dir, 'email_ports.json')
        try:
            with open(email_ports_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load email_ports.json: {str(e)}")
            return {}

config = Config()
