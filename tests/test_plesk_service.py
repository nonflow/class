import unittest
from unittest.mock import patch, Mock
from python.plesk_service import PleskService

class TestPleskService(unittest.TestCase):
    def setUp(self):
        self.service = PleskService('test_host', 'test_username', 'test_password')

    @patch('python.plesk_service.requests.post')
    def test_generate_plesk_api_key(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'key': 'test_api_key'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.service.generate_plesk_api_key()

        mock_post.assert_called_once_with(
            'https://test_host:8443/api/v2/auth/keys',
            auth=('test_username', 'test_password'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json={},
            verify=False
        )
        self.assertEqual(result, 'test_api_key')

    @patch('python.plesk_service.requests.request')
    def test_send_request(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'success'}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        result = self.service._send_request('GET', 'test_endpoint', {'data': 'test'})

        mock_request.assert_called_once_with(
            'GET',
            'https://test_host:8443/api/v2/test_endpoint',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-API-Key': self.service.api_key
            },
            json={'data': 'test'},
            verify=False
        )
        self.assertEqual(result, {'result': 'success'})

    @patch('python.plesk_service.PleskService._send_request')
    def test_list_domains(self, mock_send_request):
        mock_send_request.return_value = [
            {'name': 'domain1.com'},
            {'name': 'domain2.com'}
        ]

        result = self.service.list_domains()

        mock_send_request.assert_called_once_with('GET', 'domains')
        self.assertEqual(result, ['domain1.com', 'domain2.com'])

    @patch('python.plesk_service.PleskService._send_request')
    def test_create_database(self, mock_send_request):
        mock_send_request.return_value = {'id': 1}

        result = self.service.create_database('webspace', 'db_name', 'db_user', 'db_password')

        mock_send_request.assert_called_once_with('POST', 'databases', {
            'webspace': 'webspace',
            'name': 'db_name',
            'type': 'mysql',
            'server': 'localhost',
            'user': {
                'name': 'db_user',
                'password': 'db_password'
            }
        })
        self.assertEqual(result, 'Database created successfully')

if __name__ == '__main__':
    unittest.main()
