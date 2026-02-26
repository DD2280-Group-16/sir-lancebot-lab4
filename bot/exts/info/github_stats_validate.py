from datetime import datetime

class GitHubStatsValidate:
    # Since the comments on the issue mentioned that the stats should only come from
    # the repos:
    # - python-discord/bot
    # - python-discord/sir-lancebot
    # Added these just in case
    # - python-discord/snekbox
    # - python-discord/site
    # these are the only allowed formats
    # Possible to add more repos.
    async def validate_repo_format(self, repo_str: str) -> bool:
        """Validates that the repo is one of the allowed repos."""
        
        allowed_repos = (
            "python-discord/bot",
            "python-discord/sir-lancebot",
            "python-discord/snekbox",
            "python-discord/site"
        )
        return repo_str in allowed_repos
    
    # Went with only ISO standard. Have to change the tests.
    async def validate_date_format(self, date_str: str) -> bool:
        """Validates that the date string is formatted correctly."""
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
        
    # Validates that the given dates are in order and that they are
    # logically valid.
    async def validate_date_range(self, start_date: str, end_date: str) -> bool:
        """Validates the given date range."""
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return False
        
        time_now = datetime.now(datetime.timezone.utc)
        
        if start > end:
            return False
        
        if end > time_now:
            return False
        
        return True