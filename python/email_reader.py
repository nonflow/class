import logging
import os
import imaplib
import email
import socket
from email.header import decode_header
import time
from email_utils import parse_date

logger = logging.getLogger(__name__)

class EmailReader:
    def __init__(self, imap_server, imap_port, imap_use_ssl, username, password):
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.imap_use_ssl = imap_use_ssl
        self.username = username
        self.password = password

        if not all([self.imap_server, self.imap_port, self.username, self.password]):
            raise ValueError("Missing required email reader configuration parameters")

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

    def download_attachments(self, from_date, to_date, download_dir='attachments', folder='INBOX', max_retries=3, timeout=300):
        """
        Download all attachments from emails within the specified date range and folder.
        
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

    def delete_emails_with_filters(self, subject_filter=None, content_filter=None, from_date=None, to_date=None, folder='INBOX'):
        """
        Delete emails from the server based on specified filters.
        
        :param subject_filter: String to search for in email subject (optional)
        :param content_filter: String to search for in email content (optional) 
        :param from_date: Start date for email search (inclusive) in any recognizable date format (optional)
        :param to_date: End date for email search (inclusive) in any recognizable date format (optional)
        :param folder: Email folder to search (default: 'INBOX')
        """
        if from_date:
            from_date = parse_date(from_date)
        if to_date:
            to_date = parse_date(to_date)
        
        try:
            # Connect to the IMAP server
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap_server:
                # Login to the server
                imap_server.login(self.username, self.password)
                
                # Select the mailbox you want to delete from
                imap_server.select(folder)
                
                # Search for emails matching the filters
                criteria = []
                if from_date and to_date:
                    criteria.append(f'(SINCE "{from_date}" BEFORE "{to_date}")')
                elif from_date:
                    criteria.append(f'(SINCE "{from_date}")')
                elif to_date:
                    criteria.append(f'(BEFORE "{to_date}")')
                
                if subject_filter:
                    criteria.append(f'(SUBJECT "{subject_filter}")')
                if content_filter:
                    criteria.append(f'(BODY "{content_filter}")')
                
                _, message_numbers = imap_server.search(None, *[c.encode() for c in criteria])
                
                if message_numbers[0]:
                    # Convert message numbers to list of comma-separated strings
                    message_ids = ','.join(message_numbers[0].decode().split())
                    
                    # Delete the emails
                    imap_server.store(message_ids, '+FLAGS', '\\Deleted')
                    
                    # Expunge the mailbox to actually remove the emails
                    imap_server.expunge()
                    
                    logger.info(f"Deleted {len(message_numbers[0].split())} emails matching filters from folder: {folder}")
                else:
                    logger.info(f"No emails found matching filters in folder: {folder}")
        
        except Exception as e:
            logger.error(f"Error deleting emails: {str(e)}")


def create_email_reader(imap_server, imap_port, imap_use_ssl, username, password):
    """
    Factory method to create an EmailReader instance based on the provided parameters.
    """
    return EmailReader(imap_server, imap_port, imap_use_ssl, username, password)
