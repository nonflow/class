import unittest
from unittest.mock import patch
from datetime import datetime
from python.date_converters import current_date, previous_date

class TestDateConverters(unittest.TestCase):
    @patch('python.date_converters.datetime')
    def test_current_date(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 5, 15)
        self.assertEqual(current_date(), '2023-05-15')

    @patch('python.date_converters.datetime')
    def test_previous_date(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 5, 15)
        self.assertEqual(previous_date(), '2023-05-14')

if __name__ == '__main__':
    unittest.main()
