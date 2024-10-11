import unittest
from unittest.mock import patch, Mock, mock_open
from python.email_service import EmailService, GmailService, OutlookService
import smtplib

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.service = EmailService('test_server', 587, 'test@example.com', 'test_password')

    @patch('python.email_service.smtplib.SMTP')
    @patch('python.email_service.logger')
    def test_send_email_success(self, mock_logger, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = self.service.send_email('recipient@example.com', 'Test Subject', 'Test Body')

        mock_smtp.assert_called_once_with('test_server', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.send_message.assert_called_once()
        mock_logger.info.assert_called_once_with("Email sent successfully to recipient@example.com")
        self.assertEqual(result, "Email sent successfully")

    @patch('python.email_service.smtplib.SMTP')
    @patch('python.email_service.logger')
    def test_send_email_failure(self, mock_logger, mock_smtp):
        mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("Test error")

        result = self.service.send_email('recipient@example.com', 'Test Subject', 'Test Body')

        mock_logger.error.assert_called_once_with("Failed to send email to recipient@example.com. Error: Test error")
        self.assertEqual(result, "Failed to send email: Test error")

    @patch('python.email_service.smtplib.SMTP')
    @patch('python.email_service.logger')
    @patch('builtins.open', new_callable=mock_open, read_data=b"file content")
    def test_send_email_with_attachment(self, mock_file, mock_logger, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = self.service.send_email('recipient@example.com', 'Test Subject', 'Test Body', ['test.txt'])

        mock_smtp.assert_called_once_with('test_server', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.send_message.assert_called_once()
        mock_logger.info.assert_called_once_with("Email sent successfully to recipient@example.com")
        self.assertEqual(result, "Email sent successfully")

    @patch('python.email_service.smtplib.SMTP')
    @patch('python.email_service.logger')
    def test_send_html_email_success(self, mock_logger, mock_smtp):
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = self.service.send_html_email('recipient@example.com', 'Test Subject', '<html><body>Test HTML</body></html>')

        mock_smtp.assert_called_once_with('test_server', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@example.com', 'test_password')
        mock_server.send_message.assert_called_once()
        mock_logger.info.assert_called_once_with("HTML email sent successfully to recipient@example.com")
        self.assertEqual(result, "HTML email sent successfully")

    @patch('python.email_service.EmailService.send_email')
    def test_send_bulk_email(self, mock_send_email):
        mock_send_email.side_effect = ["Email sent successfully", "Failed to send email: Test error", "Email sent successfully"]
        
        result = self.service.send_bulk_email(['recipient1@example.com', 'recipient2@example.com', 'recipient3@example.com'], 'Test Subject', 'Test Body')

        self.assertEqual(mock_send_email.call_count, 3)
        self.assertEqual(result, "Bulk email sent. Successful: 2, Failed: 1")

class TestGmailService(unittest.TestCase):
    def test_init(self):
        service = GmailService('test@gmail.com', 'test_password')
        self.assertEqual(service.smtp_server, 'smtp.gmail.com')
        self.assertEqual(service.smtp_port, 587)
        self.assertEqual(service.username, 'test@gmail.com')
        self.assertEqual(service.password, 'test_password')

class TestOutlookService(unittest.TestCase):
    def test_init(self):
        service = OutlookService('test@outlook.com', 'test_password')
        self.assertEqual(service.smtp_server, 'smtp-mail.outlook.com')
        self.assertEqual(service.smtp_port, 587)
        self.assertEqual(service.username, 'test@outlook.com')
        self.assertEqual(service.password, 'test_password')

if __name__ == '__main__':
    unittest.main()
