import requests

class GitHubService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.github.com"

    def list_repositories(self):
        url = f"{self.base_url}/user/repos"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def create_issue(self, repo_owner, repo_name, title, body):
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": body
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
