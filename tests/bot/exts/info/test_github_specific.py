import unittest
from unittest.mock import AsyncMock, MagicMock

# from bot.exts.info import github_stats
from tests.helpers import MockBot, MockContext


# The given repo must exist to be able to gather its stats
# Creates the need for a method:
# async def repo_exists(self, repo_str: str) -> bool:
# This method would verify that the given repo exist using GitHub API and
class GitHubStatsCogRepoExistenceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = MockBot()
        #self.cog = github_stats.Stats(self.bot)
        self.bot.http_session = MagicMock()
        self.ctx = MockContext(bot=self.bot)

    async def test_repo_exists_returns_false_for_non_existent_repo(self):
        """If the GitHub API responds with 404 or raises an exception, repo_exists should return False."""

        self.bot.http_session.get = AsyncMock(side_effect=Exception("404 Not Found"))

        result = await self.cog.repo_exist("owner/non-existent-repo")

        self.assertFalse(result)

    async def test_repo_exists_returns_true_for_existent_repo(self):
        """If the GitHub API responds with JSON, repo_exists should return True."""
        self.bot.http_session.get = AsyncMock(return_value={"id":1, "name": "test"})

        result = await self.cog.repo_exists("owner/test")
        self.assertTrue(result)


# The output of the command should be the stats of the given repo.
# Example output given in the issue:
# -------------------------
# Issues opened: 20
# Issues closed: 15
# Pull Requests opened: 10
# Pull Requests closed: 2
# Pull Requests merged: 8
# Stars gained: 100
# New contributors: 10
# Commits:50
# -------------------------
# This test tests if the output is correct.
# Creates the need for five methods:
# - async def get_commit_count(self, repo_str: str, start_str: str, end_str: str) -> int
# - async def get_issue_count(self, repo_str: str, start_str: str, end_str: str) -> int
# - async def get_pr_count(self, repo_str: str, start_str: str, end_str: str) -> int
# - async def get_stars_count(self, repo_str: str, start_str: str, end_str: str) -> int
# - async def get_new_contributors_count(self, repo_str: str, start_str: str, end_str: str) -> int
#
# All these methods/functions should all grab smaller pieces of info from the repo.
class GitHubStatsCogStatsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bot = MockBot()
        self.bot.http_session = MagicMock()
        #self.cog = github_stats.Stats(self.bot)
        self.ctx = MockContext(bot=self.bot)

    # This test assumes github_stats prints out its output in the same way that the example output is:
    #
    # Name: repoName
    # Issues opened: numIssues
    # Issues closed: numClosedIssues
    # Opened PRs: numPRS
    # Closed PRs: numClosedPRS
    # Merged PRs: numMergedPRS
    # Stars gained: numStars
    # New contributors: numContributors
    # Commits: numCommits
    #
    # If we decide it should work another way, we must refactor this test
    async def test_github_stats_outputs_the_correct_stats(self):
        """Test that asserts that github_stats fetches and displays a GitHub Repo's stats correctly."""
        self.cog.get_commit_count = AsyncMock(return_value=50)
        self.cog.get_issue_count = AsyncMock(return_value=(20, 15))
        self.cog.get_pr_count = AsyncMock(return_value=(10, 2, 8))
        self.cog.get_stars_count = AsyncMock(return_value=100)
        self.cog.get_new_contributors_count = AsyncMock(return_value=10)
        # Valid repo
        self.bot.http_session.get = AsyncMock(return_value={"id":1, "name": "test"})

        await self.cog.github_stats(self.ctx, "2025-04-01", "2025-04-11", "owner/test")
        # Asserts that ctx was called with the correct message
        self.ctx.send.assert_called_once()
        sent_message = self.ctx.send.call_args.kwargs.get("content")
        expected_message = (
        "Issues opened: 20\n"
        "Issues closed: 15\n"
        "Pull Requests opened: 10\n"
        "Pull Requests closed: 2\n"
        "Pull Requests merged: 8\n"
        "Stars gained: 100\n"
        "New contributors: 10\n"
        "Commits: 50"
        )
        self.assertEqual(sent_message, expected_message)
