import requests

class CloudflareService:
    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email
        self.base_url = "https://api.cloudflare.com/client/v4/"

    def list_zones(self):
        url = f"{self.base_url}zones"
        headers = {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def purge_cache(self, zone_id):
        url = f"{self.base_url}zones/{zone_id}/purge_cache"
        headers = {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {"purge_everything": True}
        response = requests.post(url, headers=headers, json=data)
        return response.json()
