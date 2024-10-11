class Message:
    def __init__(self, account):
        self.account = account

    def create(self, to_email, subject, content):
        if not self.account.email_service:
            return "Error: No email service connected"
        return self.account.email_service.send_email(to_email, subject, content)

    def list(self, service, **kwargs):
        if service == 'cloudflare':
            if not self.account.cloudflare_service:
                return "Error: Cloudflare service not connected"
            return self.account.cloudflare_service.list_zones()
        elif service == 'gitlab':
            if not self.account.gitlab_service:
                return "Error: GitLab service not connected"
            return self.account.gitlab_service.list_projects()
        elif service == 'github':
            if not self.account.github_service:
                return "Error: GitHub service not connected"
            return self.account.github_service.list_repositories()
        elif service == 'plesk':
            if not self.account.plesk_service:
                return "Error: Plesk service not connected"
            return self.account.plesk_service.list_domains()
        else:
            return f"Error: Unsupported service for listing: {service}"

    def create_issue(self, service, **kwargs):
        if service == 'gitlab':
            if not self.account.gitlab_service:
                return "Error: GitLab service not connected"
            return self.account.gitlab_service.create_issue(kwargs['project_id'], kwargs['title'], kwargs['description'])
        elif service == 'github':
            if not self.account.github_service:
                return "Error: GitHub service not connected"
            return self.account.github_service.create_issue(kwargs['repo_owner'], kwargs['repo_name'], kwargs['title'], kwargs['body'])
        else:
            return f"Error: Unsupported service for creating issues: {service}"

    def purge_cache(self, zone_id):
        if not self.account.cloudflare_service:
            return "Error: Cloudflare service not connected"
        return self.account.cloudflare_service.purge_cache(zone_id)

    def create_database(self, webspace_name, db_name, db_user, db_password):
        if not self.account.plesk_service:
            return "Error: Plesk service not connected"
        return self.account.plesk_service.create_database(webspace_name, db_name, db_user, db_password)
