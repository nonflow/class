import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.github.com"

    def _get_repositories(self):
        url = f"{self.base_url}/user/repos"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching repositories: {e}")
            return None

    def list_all_repositories(self):
        """
        List all GitHub repositories for the authenticated user.

        :return: List of all repositories or None if the request failed
        """
        return self._get_repositories()

    def list_repositories(self, filter_key='name', filter_value=None):
        """
        List GitHub repositories for the authenticated user, with optional filtering.

        :param filter_key: The repository attribute to filter on (default: 'name')
        :param filter_value: The value to filter for. If None, no filtering is applied.
        :return: List of repositories (filtered if filter_value is provided) or None if the request failed
        """
        repos = self._get_repositories()
        if repos is None:
            return None

        if filter_value is not None:
            filtered_repos = [
                repo for repo in repos
                if str(repo.get(filter_key, '')).lower() == str(filter_value).lower()
            ]
            return filtered_repos
        else:
            return repos

    def create_issue(self, repo_owner, repo_name, title, body):
        """
        Create an issue in a GitHub repository.

        :param repo_owner: Owner of the repository
        :param repo_name: Name of the repository
        :param title: Title of the issue
        :param body: Body content of the issue
        :return: Created issue data or None if the request failed
        """
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": body
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error creating issue: {e}")
            return None
