from discord.ext.commands import Cog, command, Context
from bot.constants import Tokens
from bot.bot import Bot

GITHUB_API_URL = "https://api.github.com"


class GitHubStats(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="gh-stats")
    async def github_stats(self, ctx: Context, start: str, end: str, repo: str = "python-discord/sir-lancebot") -> None:
        """
        Fetches stats for a GitHub repo.
        Usage: !github_stats 2023-01-01 2023-12-31 python-discord/bot
        """
        if not await self.repo_exists(repo):
            await ctx.send(f"❌ Could not find repository: `{repo}`")
            return

        open = await self.get_issue_count(repo, start, end, state="created")
        closed = await self.get_issue_count(repo, start, end, state="closed")
        stars_gained = await self.get_stars_gained(repo, start, end)

        stats_message = (
            f"Stats for **{repo}** ({start} to {end}):\n" f"Issues opened: {open}\n" f"Issues closed: {closed}\n" f"Stars gained: +{stars_gained}\n"
        )
        await ctx.send(stats_message)

    async def repo_exists(self, repo: str) -> bool:
        """
        Checks if a repository exists on GitHub.

        Args:
            repo (str): The repository name in 'owner/repo' format (e.g., 'python-discord/bot').
        """
        url = f"{GITHUB_API_URL}/repos/{repo}"
        headers = {"Authorization": f"token {Tokens.github.get_secret_value()}"}

        async with self.bot.http_session.get(url, headers=headers) as response:
            return response.status == 200

    async def get_issue_count(self, repo: str, start: str, end: str, state: str) -> int:
        """
        Gets the number of issues opened or closed (based on state) in a given timeframe.

        Args:
            repo (str): The repository name in 'owner/repo' format (e.g., 'python-discord/bot').
            start (str): The start date (e.g., 2023-01-01).
            end (str): The end date (e.g., 2023-12-31).
            state (str): The state of the issue (created/closed)
        """
        url = f"{GITHUB_API_URL}/search/issues"
        headers = {"Authorization": f"token {Tokens.github.get_secret_value()}"}

        # The query string uses GitHub's advanced search syntax
        # e.g., repo:python-discord/bot is:issue created:2023-01-01..2023-12-31
        query = f"repo:{repo} is:issue {state}:{start}..{end}"
        params = {"q": query}

        async with self.bot.http_session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                return -1

            data = await response.json()
            return data.get("total_count", 0)

    async def get_stars_gained(self, repo: str, start: str, end: str) -> int:
        """Gets the number of stars gained for a given repository in a timeframe.
        Args:
            repo (str): The repository name in 'owner/repo' format (e.g., 'python-discord/bot').
            start (str): The start date (e.g., 2023-01-01).
            end (str): The end date (e.g., 2023-12-31).
        """
        url = f"{GITHUB_API_URL}/repos/{repo}/stargazers"
        headers = {
            "Authorization": f"token {Tokens.github.get_secret_value()}",
            "Accept": "application/vnd.github.star+json",
        }
        count = 0
        page = 1
        per_page = 100

        while True:
            params = {"per_page": per_page, "page": page}
            async with self.bot.http_session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    return -1
                data = await response.json()
                if not data:
                    break
                # starred_at is in format YYYY-MM-DDTHH:MM:SSZ so we can just get the first 10 characters to get the date
                count += sum(1 for star in data if start <= star.get("starred_at", "")[:10] <= end)
                if len(data) < per_page:
                    break
                page += 1

        return count
async def setup(bot: Bot) -> None:
    await bot.add_cog(GitHubStats(bot))
