import unittest
from unittest.mock import patch, Mock
from python.github_service import GitHubService

class TestGitHubService(unittest.TestCase):
    def setUp(self):
        self.service = GitHubService('test_access_token')

    @patch('python.github_service.requests.get')
    def test_get_repositories(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{'id': 1, 'name': 'Repo 1'}, {'id': 2, 'name': 'Repo 2'}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.service._get_repositories()

        mock_get.assert_called_once_with(
            'https://api.github.com/user/repos',
            headers={
                'Authorization': 'token test_access_token',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        self.assertEqual(result, [{'id': 1, 'name': 'Repo 1'}, {'id': 2, 'name': 'Repo 2'}])

    @patch('python.github_service.GitHubService._get_repositories')
    def test_list_all_repositories(self, mock_get_repositories):
        mock_get_repositories.return_value = [{'id': 1, 'name': 'Repo 1'}, {'id': 2, 'name': 'Repo 2'}]

        result = self.service.list_all_repositories()

        self.assertEqual(result, [{'id': 1, 'name': 'Repo 1'}, {'id': 2, 'name': 'Repo 2'}])

    @patch('python.github_service.GitHubService._get_repositories')
    def test_list_repositories_with_filter(self, mock_get_repositories):
        mock_get_repositories.return_value = [
            {'id': 1, 'name': 'Repo 1'},
            {'id': 2, 'name': 'Repo 2'},
            {'id': 3, 'name': 'Test Repo'}
        ]

        result = self.service.list_repositories(filter_key='name', filter_value='Test Repo')

        self.assertEqual(result, [{'id': 3, 'name': 'Test Repo'}])

    @patch('python.github_service.requests.post')
    def test_create_issue(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'id': 1, 'title': 'Test Issue', 'body': 'Test Body'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.service.create_issue('owner', 'repo', 'Test Issue', 'Test Body')

        mock_post.assert_called_once_with(
            'https://api.github.com/repos/owner/repo/issues',
            headers={
                'Authorization': 'token test_access_token',
                'Accept': 'application/vnd.github.v3+json'
            },
            json={'title': 'Test Issue', 'body': 'Test Body'}
        )
        self.assertEqual(result, {'id': 1, 'title': 'Test Issue', 'body': 'Test Body'})

if __name__ == '__main__':
    unittest.main()
