import unittest

# from bot.exts.info import github_stats
from tests.helpers import MockBot, MockContext

# Repo format: owner/repo
# Method name could be:
# async def validate_repo_format(self, repo_str: str) -> bool:
# This method should test the given string if its formatted correctly

class GitStatsCogTestRepoFormat(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Attach an instance of the cog to the class for tests."""
        self.bot = MockBot()
        # self.cog = github_stats.Stats(self.bot)
        self.ctx = MockContext(bot=self.bot)

    async def test_validate_repo_format_accepts_valid_formats(self):
        """Valid repo strings should be accepted"""
        valid_repos = (
            "owner/repo", # The accepted style
            "12345/12345", # The repo can contain numbers
            "abc-sd/123", # The repo may contain dashes
            ".abc/repo", # Dots are accepted
            "_abc/repo", # Underline are accepted
        )

        for repo_str in valid_repos:
            with self.subTest(repo=repo_str):
                    result = await self.cog.validate_repo_format(repo_str)
                    self.assertTrue(result)

    async def test_validate_repo_format_rejects_invalid_formats(self):
        """Invalid repo strings should be rejected"""
        invalid_repos = (
            "owner-repo", # Invalid separator
            "owner.repo", # Invalid separator
            "owner_repo", # Invalid separator
            "ownerrepo", # No separator
            "owner//repo", # Double separator
            "", # Empty string
        )

        for repo_str in invalid_repos:
            with self.subTest(repo=repo_str):
                result = await self.cog.validate_repo_format(repo_str)
                self.assertFalse(result)
