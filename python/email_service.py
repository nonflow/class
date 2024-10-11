import smtplib
import logging
import socket
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def check_ports(self, host, ports):
        results = {}
        for port in ports:
            try:
                with socket.create_connection((host, port), timeout=2) as sock:
                    results[port] = "Open"
            except socket.error as e:
                if e.errno == 111:  # Connection refused
                    results[port] = "Connection refused"
                else:
                    results[port] = f"Error: {e}"
        return results


    def test(self):
        # Define email ports
        email_ports = [25, 465, 587, 110, 143, 993]  # Only include relevant email ports
        host_to_check = self.smtp_server
        port_results = self.check_ports(host_to_check, email_ports)

        for port, status in port_results.items():
            print(f"Port {port}: {status}")

    def send_email(self, to_email, subject, body, is_html=False):
        if not is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        # msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return "Email sent successfully"
        except smtplib.SMTPAuthenticationError:
            logger.error("Authentication failed. Check your username and password.")
            return "Authentication failed"
        except smtplib.SMTPConnectError:
            logger.error("Failed to connect to the server.")
            return "Connection error"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")
            return f"Failed to send email: {str(e)}"


class GmailService(EmailService):
    def __init__(self, username, password):
        super().__init__('smtp.gmail.com', 587, username, password)

class OutlookService(EmailService):
    def __init__(self, username, password):
        super().__init__('smtp-mail.outlook.com', 587, username, password)


