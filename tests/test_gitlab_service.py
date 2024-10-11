import unittest
from unittest.mock import patch, Mock
from python.gitlab_service import GitLabService

class TestGitLabService(unittest.TestCase):
    def setUp(self):
        self.service = GitLabService('https://gitlab.com', 'test_private_token')

    @patch('python.gitlab_service.requests.get')
    def test_list_projects(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}]
        mock_get.return_value = mock_response

        result = self.service.list_projects()

        mock_get.assert_called_once_with(
            'https://gitlab.com/api/v4/projects',
            headers={'Private-Token': 'test_private_token'}
        )
        self.assertEqual(result, [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}])

    @patch('python.gitlab_service.requests.post')
    def test_create_issue(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'id': 1, 'title': 'Test Issue', 'description': 'Test Description'}
        mock_post.return_value = mock_response

        result = self.service.create_issue(1, 'Test Issue', 'Test Description')

        mock_post.assert_called_once_with(
            'https://gitlab.com/api/v4/projects/1/issues',
            headers={'Private-Token': 'test_private_token'},
            json={'title': 'Test Issue', 'description': 'Test Description'}
        )
        self.assertEqual(result, {'id': 1, 'title': 'Test Issue', 'description': 'Test Description'})

if __name__ == '__main__':
    unittest.main()
