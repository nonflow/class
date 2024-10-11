import smtplib
import logging
import socket
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

logger = logging.getLogger(__name__)

email_ports = {
    25: {"protocol": "SMTP", "security": "Unencrypted", },
    465: {"protocol": "SMTP", "security": "SSL" },
    587: {"protocol": "SMTP", "security": "TLS" },
    2525: {"protocol": "SMTP", "security": "Alternative" },
    110: {"protocol": "POP3", "security": "Unencrypted" },
    995: {"protocol": "POP3", "security": "SSL" },
    143: {"protocol": "IMAP", "security": "Unencrypted" },
    993: {"protocol": "IMAP", "security": "SSL" }
}



class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

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
        # Extract ports from the email_ports dictionary
        email_ports_no = list(email_ports.keys())

        # Use the SMTP server address for testing
        host_to_check = self.smtp_server

        # Check the ports and get results
        port_results = self.check_ports(host_to_check, email_ports_no)

        # Prepare result string
        result = ""
        for port in email_ports_no:
            protocol_info = email_ports[port]
            status = port_results.get(port, "Unknown")
            result += f"{protocol_info['protocol']} {protocol_info['security']} Port {port}: {status}\n"

        return result

    def send_email(self, to_email, subject, body, is_html=False, attachments = []):
        if not self.is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return "Email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")
            return f"Failed to send email: {str(e)}"

    def send_email_with_attachments(self, to_email, subject, body, attachments):
        if not self.is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]

            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Email sent successfully to {to_email}")
            return "Email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email to {to_email}. Error: {str(e)}")
            return f"Failed to send email: {str(e)}"

    def send_html_email(self, to_email, subject, html_body):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"HTML email sent successfully to {to_email}")
            return "HTML email sent successfully"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send HTML email to {to_email}. Error: {str(e)}")
            return f"Failed to send HTML email: {str(e)}"

    def send_bulk_email(self, to_emails, subject, body):
        successful_sends = 0
        failed_sends = 0

        for email in to_emails:
            result = self.send_email(email, subject, body)
            if "successfully" in result:
                successful_sends += 1
            else:
                failed_sends += 1

        return f"Bulk email sent. Successful: {successful_sends}, Failed: {failed_sends}"

class GmailService(EmailService):
    def __init__(self, username, password):
        super().__init__('smtp.gmail.com', 587, username, password)

class OutlookService(EmailService):
    def __init__(self, username, password):
        super().__init__('smtp-mail.outlook.com', 587, username, password)

