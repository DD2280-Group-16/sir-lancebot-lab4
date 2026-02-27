import unittest
from unittest.mock import AsyncMock, MagicMock
from tests.helpers import MockBot, MockContext
#from bot.exts.info import github_stats



# The return value from the helper functions must be from the given time frame. 
# All tests below have examples of repos with elements inside and outside the given time frame 
# Tests the methods: get_commit_count, get_issue_count, get_pr_count and get_stars_count. 

class GitHubStatsCogStatsInTimeFrame(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.bot = MockBot()

        #self.cog = GitHubStats(self.bot)
        self.bot.http_session = MagicMock()
        self.ctx = MockContext(bot=self.bot)
        
    async def test_validate_commits_in_time_frame(self):

        self.bot.http_session.get = AsyncMock(
            return_value=[
                {
                    "sha": "a",
                    "commit": {"author": {"date": "2025-12-31T23:59:59Z"}},
                },
                {
                    "sha": "b",
                    "commit": {"author": {"date": "2026-01-01T00:00:00Z"}},
                },
                {
                    "sha": "c",
                    "commit": {"author": {"date": "2026-01-03T00:00:00Z"}},
                },
            ]
        )

        result = await self.cog.get_commit_count(
            "owner/test", "2026-01-01", "2026-01-02"
        )
        self.assertEqual(result, 1)

    async def test_validate_issues_in_time_frame(self):
        self.bot.http_session.get = AsyncMock(
            return_value=[
                {
                    "number": 1,
                    "state": "open",
                    "created_at": "2026-01-01T10:00:00Z",
                    "pull_request": None,
                },
                {
                    "number": 2,
                    "state": "closed",
                    "created_at": "2026-01-02T12:00:00Z",
                    "pull_request": None,
                },
                {
                    "number": 3,
                    "state": "closed",
                    "created_at": "2026-01-03T12:00:00Z",
                    "pull_request": None,
                },
            ]
        )

        result = await self.cog.get_issue_count(
            "owner/test", "2026-01-01", "2026-01-02"
        )
        self.assertEqual(result, 2)

    async def test_validate_prs_in_time_frame(self):
        self.bot.http_session.get = AsyncMock(
            return_value=[
                {"number": 10, "created_at": "2026-01-01T09:00:00Z", "merged_at": None},
                {
                    "number": 11,
                    "created_at": "2026-01-02T11:00:00Z",
                    "merged_at": "2026-01-02T12:00:00Z",
                },
                {"number": 12, "created_at": "2026-01-03T10:00:00Z", "merged_at": None},
            ]
        )

        result = await self.cog.get_pr_count("owner/test", "2026-01-02", "2026-01-02")
        self.assertEqual(result, 1)

    async def test_validate_stars_in_time_frame(self):
        self.bot.http_session.get = AsyncMock(
            return_value=[
                {"starred_at": "2025-12-31T23:59:59Z", "user": {"login": "a"}},
                {"starred_at": "2026-01-01T08:00:00Z", "user": {"login": "b"}},
                {"starred_at": "2026-01-01T20:30:00Z", "user": {"login": "c"}},
                {"starred_at": "2026-01-03T00:00:01Z", "user": {"login": "d"}},
            ]
        )

        result = await self.cog.get_stars_count(
            "owner/test", "2026-01-01", "2026-01-02"
        )
        self.assertEqual(result, 2)
