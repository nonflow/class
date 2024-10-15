import os

from email_sender import EmailSender, create_email_sender
from email_reader import EmailReader, create_email_reader
from email_utils import load_email_ports, check_ports

email_ports = load_email_ports()

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_use_tls, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_use_tls = smtp_use_tls
        self.username = username
        self.password = password

        if not all([self.smtp_server, self.smtp_port, self.imap_server, self.imap_port, self.username, self.password]):
            raise ValueError("Missing required email configuration parameters")

    def test(self):
        # Extract ports from the email_ports dictionary
        email_ports_no = list(map(int, email_ports.keys()))

        # Use the SMTP server address for testing
        host_to_check = self.smtp_server

        # Check the ports and get results
        port_results = check_ports(host_to_check, email_ports_no)

        # Prepare result string
        result = ""
        for port in email_ports_no:
            protocol_info = email_ports[str(port)]
            status = port_results.get(port, "Unknown")
            result += f"{protocol_info['protocol']} {protocol_info['security']} Port {port}: {status}\n"

        return result


    def remove_files_with_filters(self, subject_filter=None, content_filter=None,
                                  from_date=None, to_date=None):
        """Removes email files based on the provided filters.

        Args:
            subject_filter: A string to search for in the email subject.
            content_filter: A string to search for in the email content.
            from_date: The start date for filtering emails (inclusive).
            to_date: The end date for filtering emails (inclusive).
        """
        for filename in os.listdir(self.download_folder):
            filepath = os.path.join(self.download_folder, filename)
            if not os.path.isfile(filepath):
                continue

            with open(filepath, "r") as f:
                msg = email.message_from_file(f)

            subject = msg["Subject"]
            content = msg.get_payload(decode=True).decode()
            date_sent = email.utils.parsedate_to_datetime(msg["Date"])

            if subject_filter and subject_filter not in subject:
                continue
            if content_filter and content_filter not in content:
                continue
            if from_date and date_sent < from_date:
                continue
            if to_date and date_sent > to_date:
                continue

            os.remove(filepath)
            print(f"Removed: {filename}")

# Example of how to use the email services:
# 
# def send_email_example(config):
#     sender = create_email_sender(
#         smtp_server=config['smtp_server'],
#         smtp_port=config['smtp_port'],
#         smtp_use_tls=config['smtp_use_tls'],
#         username=config['username'],
#         password=config['password']
#     )
#     return sender.send_email(to_email, subject, body)
# 
# def read_emails_example(config):
#     reader = create_email_reader(
#         imap_server=config['imap_server'],
#         imap_port=config['imap_port'],
#         imap_use_ssl=config['imap_use_ssl'],
#         username=config['username'],
#         password=config['password']
#     )
#     return reader.list_emails(from_date, to_date)
