from email_service import GmailService, OutlookService
from cloudflare_service import CloudflareService
from gitlab_service import GitLabService
from github_service import GitHubService
from plesk_service import PleskService

class Account:
    def __init__(self):
        self.email_service = None
        self.cloudflare_service = None
        self.gitlab_service = None
        self.github_service = None
        self.plesk_service = None

    def connect(self, service_type, **kwargs):
        if service_type == 'GmailService':
            self.email_service = GmailService(kwargs['username'], kwargs['password'])
        elif service_type == 'OutlookService':
            self.email_service = OutlookService(kwargs['username'], kwargs['password'])
        elif service_type == 'CloudflareService':
            self.cloudflare_service = CloudflareService(kwargs['api_key'], kwargs['email'])
        elif service_type == 'GitLabService':
            self.gitlab_service = GitLabService(kwargs['base_url'], kwargs['private_token'])
        elif service_type == 'GitHubService':
            self.github_service = GitHubService(kwargs['access_token'])
        elif service_type == 'PleskService':
            self.plesk_service = PleskService(kwargs['host'], kwargs['username'], kwargs['password'])
        else:
            raise ValueError(f"Unsupported service type: {service_type}")
        
        return f"Connected to {service_type} successfully"

    def disconnect(self, service_type):
        if service_type in ['GmailService', 'OutlookService']:
            self.email_service = None
        elif service_type == 'CloudflareService':
            self.cloudflare_service = None
        elif service_type == 'GitLabService':
            self.gitlab_service = None
        elif service_type == 'GitHubService':
            self.github_service = None
        elif service_type == 'PleskService':
            self.plesk_service = None
        else:
            raise ValueError(f"Unsupported service type: {service_type}")
        
        return f"Disconnected from {service_type} successfully"
