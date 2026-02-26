from bot.constants import Tokens
from bot.bot import Bot

class GitStatsGetCommitsMethod:
    def __init__(self, bot):
        self.bot = bot
        
    # GitHub API for commits:
    # https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits
    #
    # When we get to this stage in the command, we already know that:
    # repo_str, start_str and end_str are formatted correctly. We also know that the repo exists so all we need 
    # to do is to make the API call.
    async def get_commit_count(self, repo_str: str, start_str: str, end_str: str) -> int:
        """Returns the number of commits done to the given repo between the start- and end-date."""
        
        # Number of commits
        count = 0
        # per_page is the number of results per page. Max 100
        per_page = 100
        # Page number with default = 1
        page = 1
        # Formatting in ISO8601 standard:
        # YYYY-MM-DDTHH:MM:SSZ
        start_iso = f"{start_str}T00:00:00Z"
        end_iso = f"{end_str}T00:00:00Z"
        
        headers = {"Authorization": f"token {Tokens.github.get_secret_value()}"}
        
        while True:
            url = (
                f"https://api.github.com/repos/{repo_str}/commits"
                f"?since={start_iso}&until={end_iso}&per_page={per_page}&page={page}"
            )
            
            async with self.bot.http_session.get(url, headers=headers) as response:
                commits_json = await response.json()
                # GitHub API responds with a JSON list of commits
                # and we add the number of items in the list to count
                count += len(commits_json)
                # Max 100 per page so if its less, we have reached the end
                if len(commits_json) < per_page:
                    break
                # Else we "turn" the page
                page += 1
                
        return count