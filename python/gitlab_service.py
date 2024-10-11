import requests

class GitLabService:
    def __init__(self, base_url, private_token):
        self.base_url = base_url
        self.private_token = private_token

    def list_projects(self):
        url = f"{self.base_url}/api/v4/projects"
        headers = {"Private-Token": self.private_token}
        response = requests.get(url, headers=headers)
        return response.json()

    def create_issue(self, project_id, title, description):
        url = f"{self.base_url}/api/v4/projects/{project_id}/issues"
        headers = {"Private-Token": self.private_token}
        data = {
            "title": title,
            "description": description
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
