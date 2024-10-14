import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_utils import is_valid_email

logger = logging.getLogger(__name__)
#TODO: save to draft
#TODO: send from draft
class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_use_tls, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_use_tls = smtp_use_tls
        self.username = username
        self.password = password

        if not all([self.smtp_server, self.smtp_port, self.username, self.password]):
            raise ValueError("Missing required email sender configuration parameters")

    def send_email(self, to_email, subject, body, is_html=False, attachments=[]):
        if not is_valid_email(to_email):
            logger.error(f"Invalid email address: {to_email}")
            return "Invalid email address"

        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_use_tls:
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

def create_email_sender(smtp_server, smtp_port, smtp_use_tls, username, password):
    """
    Factory method to create an EmailSender instance based on the provided parameters.
    """
    return EmailSender(smtp_server, smtp_port, smtp_use_tls, username, password)
