import yaml

class Account:
    def __init__(self):
        self.connected = False
        self.email = None

    def connect(self, email):
        try:
            with open('private.yaml', 'r') as file:
                private_data = yaml.safe_load(file)
            
            if email in private_data:
                self.email = email
                self.connected = True
                print(f"Connected to account: {email}")
                return True
            else:
                print(f"No data found for email: {email}")
                return False
        except FileNotFoundError:
            print("Error: private.yaml file not found")
            return False

    def disconnect(self):
        if self.connected:
            self.connected = False
            print(f"Disconnected from account: {self.email}")
            self.email = None
            return True
        else:
            print("No active connection to disconnect")
            return False