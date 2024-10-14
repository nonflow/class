import smtplib
import logging
import socket
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import imaplib
import email
from email.header import decode_header
import json
import base64
from dateutil import parser
import time

logger = logging.getLogger(__name__)

def load_email_ports():
    try:
        with open('python/email_ports.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load email_ports.json: {str(e)}")
        return {}

email_ports = load_email_ports()

def parse_date(date_string):
    """
    Parse a date string in various formats and return it in 'DD-MMM-YYYY' format.
    
    :param date_string: A string representing a date
    :return: A string representing the date in 'DD-MMM-YYYY' format
    """
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime('%d-%b-%Y')
    except ValueError:
        logger.error(f"Unable to parse date: {date_string}")
        return None

class EmailService:
    def __init__(self, smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_use_tls = smtp_use_tls
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.imap_use_ssl = imap_use_ssl
        self.username = username
        self.password = password

        if not all([self.smtp_server, self.smtp_port, self.imap_server, self.imap_port, self.username, self.password]):
            raise ValueError("Missing required email configuration parameters")

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
        email_ports_no = list(map(int, email_ports.keys()))

        # Use the SMTP server address for testing
        host_to_check = self.smtp_server

        # Check the ports and get results
        port_results = self.check_ports(host_to_check, email_ports_no)

        # Prepare result string
        result = ""
        for port in email_ports_no:
            protocol_info = email_ports[str(port)]
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

    def list_emails(self, from_date, to_date):
        """
        List all emails between the specified date range.

        :param from_date: Start date for email search (inclusive) in any recognizable date format
        :param to_date: End date for email search (inclusive) in any recognizable date format
        :return: List of email objects
        """
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)

        if not from_date or not to_date:
            return "Invalid date format"

        logger.info(f"Listing emails from {from_date} to {to_date}")

        emails = []
        try:
            # Connect to the IMAP server
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap_server:
                # Login to the server
                imap_server.login(self.username, self.password)

                # Select the mailbox you want to read from
                imap_server.select('INBOX')

                # Search for emails within the date range
                _, message_numbers = imap_server.search(None, f'(SINCE "{from_date}" BEFORE "{to_date}")')

                for num in message_numbers[0].split():
                    # Fetch the email message by ID
                    _, msg = imap_server.fetch(num, '(RFC822)')

                    for response in msg:
                        if isinstance(response, tuple):
                            # Parse the email content
                            email_msg = email.message_from_bytes(response[1])

                            # Decode the email subject
                            subject, encoding = decode_header(email_msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or "utf-8")

                            # Get the sender
                            from_ = email_msg["From"]

                            # Get the date
                            date_ = email_msg["Date"]

                            # Get the body
                            if email_msg.is_multipart():
                                for part in email_msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                body = email_msg.get_payload(decode=True).decode()

                            # Append the email details to our list
                            emails.append({
                                "subject": subject,
                                "from": from_,
                                "date": date_,
                                "body": body[:100] + "..."  # Truncate body for brevity
                            })

        except Exception as e:
            logger.error(f"Error listing emails: {str(e)}")
            return f"Failed to list emails: {str(e)}"

        return emails

    def download_attachments(self, from_date, to_date, download_dir='attachments', max_retries=3, timeout=300):
        """
        Download all attachments from emails within the specified date range.
        
        :param from_date: Start date for email search (inclusive) in any recognizable date format
        :param to_date: End date for email search (inclusive) in any recognizable date format
        :param download_dir: Directory to save attachments (default: 'attachments')
        :param folder: Email folder to search (default: 'INBOX', use '*' for all folders)
        :param max_retries: Maximum number of connection attempts (default: 3)
        :param timeout: Connection timeout in seconds (default: 300)
        :return: List of downloaded attachment filenames or error message
        """
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        
        if not from_date or not to_date:
            return "Invalid date format"
        
        logger.info(f"Downloading attachments from {from_date} to {to_date} in folder: {folder}")
        
        downloaded_files = []
        
        for attempt in range(max_retries):
            try:
                # Create download directory if it doesn't exist
                os.makedirs(download_dir, exist_ok=True)
                
                # Connect to the IMAP server
                with imaplib.IMAP4_SSL(self.imap_server, self.imap_port, timeout=timeout) as imap_server:
                    # Login to the server
                    imap_server.login(self.username, self.password)
                    
                    # Get list of folders to search
                    folders_to_search = [folder]
                    if folder == '*':
                        _, folder_list = imap_server.list()
                        folders_to_search = [f.decode().split('"/"')[-1].strip() for f in folder_list]
                    
                    for current_folder in folders_to_search:
                        # Select the mailbox you want to read from
                        imap_server.select(current_folder)
                        
                        # Search for emails within the date range
                        _, message_numbers = imap_server.search(None, f'(SINCE "{from_date}" BEFORE "{to_date}")')
                        
                        for num in message_numbers[0].split():
                            # Fetch the email message by ID
                            _, msg = imap_server.fetch(num, '(RFC822)')
                            
                            for response in msg:
                                if isinstance(response, tuple):
                                    # Parse the email content
                                    email_msg = email.message_from_bytes(response[1])
                                    
                                    # Download attachments
                                    for part in email_msg.walk():
                                        if part.get_content_maintype() == 'multipart':
                                            continue
                                        if part.get('Content-Disposition') is None:
                                            continue

                                        filename = part.get_filename()
                                        if filename:
                                            filepath = os.path.join(download_dir, filename)
                                            with open(filepath, 'wb') as f:
                                                f.write(part.get_payload(decode=True))
                                            downloaded_files.append(filepath)
                                            logger.info(f"Downloaded: {filepath} from folder: {current_folder}")
                
                # If we've reached this point, the operation was successful
                return downloaded_files
            
            except (socket.timeout, imaplib.IMAP4.abort) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    logger.error(f"Failed to download attachments after {max_retries} attempts: {str(e)}")
                    return f"Failed to download attachments: {str(e)}"
            
            except Exception as e:
                logger.error(f"Unexpected error downloading attachments: {str(e)}")
                return f"Failed to download attachments: {str(e)}"

def create_email_service(smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password):
    """
    Factory method to create an EmailService instance based on the provided parameters.
    """
    return EmailService(smtp_server, smtp_port, smtp_use_tls, imap_server, imap_port, imap_use_ssl, username, password)

# The GmailService and OutlookService classes are no longer needed as we're using a generic EmailService
# with specific configurations. You can remove these classes if they're not used elsewhere in your code.
