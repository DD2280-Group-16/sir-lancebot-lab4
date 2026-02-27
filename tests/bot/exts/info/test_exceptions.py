import unittest
from unittest.mock import AsyncMock, MagicMock
from tests.helpers import MockBot, MockContext

# from bot.exts.info import github_stats

# The return value from the helper functions must be from the given time frame.
# All tests below have examples of repos with elements inside and outside the given time frame
# Tests the methods: get_commit_count, get_issue_count, get_pr_count and get_stars_count.

# getters
# nothing at all (commits or issues)
# wrong format API repo

# do we need to test the getters if the validators make sure that the arguments are valid?

# validators
# arguments
# null
# negative numbers
#

class GitHubStatsCogExceptions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.bot = MockBot()

        # self.cog = GitHubStats(self.bot)
        self.bot.http_session = MagicMock()
        self.ctx = MockContext(bot=self.bot)

    async def test_no_commits(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {
                        "sha": "a",
                    }
                ]
            )

            result = await self.cog.get_commit_count(
                "owner/test", "2026-01-01", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_faulty_issue_JSON(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {
                        "number": 1,
                        "state": "open",
                        "created_at": "",
                    },
                ]
            )

            result = await self.cog.get_issue_count(
                "owner/test", "2026-01-01", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_negative_issue_number(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {
                        "number": -3,
                        "state": "open",
                        "created_at": "2026-01-01T10:00:00Z",
                    },
                ]
            )

            result = await self.cog.get_issue_count(
                "owner/test", "2026-01-01", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_negative_no_pr(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(return_value=[])

            result = await self.cog.get_pr_count(
                "owner/test", "2026-01-02", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_negative_pr_number(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {
                        "number": -2,
                        "created_at": "2026-01-01T09:00:00Z",
                        "merged_at": None,
                    },
                    {
                        "number": 12,
                        "created_at": "2026-01-03T10:00:00Z",
                        "merged_at": None,
                    },
                ]
            )

            result = await self.cog.get_pr_count(
                "owner/test", "2026-01-02", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_star_user_exists(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {"starred_at": "2025-12-31T23:59:59Z", "user": {"login": ""}},
                    {"starred_at": "2026-01-01T08:00:00Z", "user": {"login": "b"}},
                    {"starred_at": "2026-01-01T20:30:00Z", "user": {"login": "c"}},
                    {"starred_at": "2026-01-03T00:00:01Z", "user": {"login": "d"}},
                ]
            )

            result = await self.cog.get_stars_count(
                "owner/test", "2026-01-01", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)

    async def test_star_future_dates(self):
        with self.assertRaises(ValueError):

            self.bot.http_session.get = AsyncMock(
                return_value=[
                    {"starred_at": "2044-12-31T23:59:59Z", "user": {"login": "a"}},
                ]
            )

            result = await self.cog.get_stars_count(
                "owner/test", "2026-01-01", "2026-01-02"
            )
        self.assertRaises(expected_exception=ValueError)
