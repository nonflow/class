import unittest
from unittest.mock import patch
from email_service.email_utils import parse_date, check_ports, is_valid_email, get_email_ports

class TestEmailUtils(unittest.TestCase):

    def test_parse_date(self):
        self.assertEqual(parse_date("2023-05-15"), "15-May-2023")
        self.assertEqual(parse_date("15/05/2023"), "15-May-2023")
        self.assertEqual(parse_date("May 15, 2023"), "15-May-2023")
        self.assertIsNone(parse_date("invalid date"))

    @patch('socket.create_connection')
    def test_check_ports(self, mock_create_connection):
        mock_create_connection.return_value.__enter__.return_value = None
        result = check_ports('example.com', [80, 443])
        self.assertEqual(result, {80: 'Open', 443: 'Open'})

        mock_create_connection.side_effect = ConnectionRefusedError
        result = check_ports('example.com', [80, 443])
        self.assertEqual(result, {80: 'Connection refused', 443: 'Connection refused'})

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email('user@example.com'))
        self.assertFalse(is_valid_email('invalid_email'))
        self.assertFalse(is_valid_email('user@example'))
        self.assertFalse(is_valid_email('@example.com'))

    @patch('email_service.config.Config.email_ports', {'25': {'protocol': 'SMTP', 'security': 'None'}})
    def test_get_email_ports(self):
        self.assertEqual(get_email_ports(), {'25': {'protocol': 'SMTP', 'security': 'None'}})

if __name__ == '__main__':
    unittest.main()
