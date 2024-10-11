import unittest
from unittest.mock import patch, Mock
from python.cloudflare_service import CloudflareService

class TestCloudflareService(unittest.TestCase):
    def setUp(self):
        self.service = CloudflareService('test_api_key', 'test@example.com')

    @patch('python.cloudflare_service.requests.get')
    def test_list_zones(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'result': ['zone1', 'zone2']}
        mock_get.return_value = mock_response

        result = self.service.list_zones()

        mock_get.assert_called_once_with(
            'https://api.cloudflare.com/client/v4/zones',
            headers={
                'X-Auth-Email': 'test@example.com',
                'X-Auth-Key': 'test_api_key',
                'Content-Type': 'application/json'
            }
        )
        self.assertEqual(result, {'result': ['zone1', 'zone2']})

    @patch('python.cloudflare_service.requests.post')
    def test_purge_cache(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response

        result = self.service.purge_cache('test_zone_id')

        mock_post.assert_called_once_with(
            'https://api.cloudflare.com/client/v4/zones/test_zone_id/purge_cache',
            headers={
                'X-Auth-Email': 'test@example.com',
                'X-Auth-Key': 'test_api_key',
                'Content-Type': 'application/json'
            },
            json={'purge_everything': True}
        )
        self.assertEqual(result, {'success': True})

if __name__ == '__main__':
    unittest.main()
