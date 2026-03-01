import unittest
from unittest.mock import AsyncMock, MagicMock

from bot.exts.utilities.githubinfo import GithubInfo
<<<<<<< HEAD

=======
>>>>>>> 1641d55f7801668eecf8d9fc544ce605f428e410
# from bot.exts.utilities.githubinfo import validate_date_format

class TestGithubStatsFeatures(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        """Set up the mock bot and cog for each test."""
        self.bot = MagicMock()
        self.bot.http_session = MagicMock()
        self.cog = GithubInfo(self.bot)

    def _create_mock_response(self, status=200, json_data=None, headers=None, links=None):
        """Helper to create a fake aiohttp response object."""
        mock_resp = AsyncMock()
        mock_resp.status = status
        mock_resp.json = AsyncMock(return_value=json_data or {})
        mock_resp.headers = headers or {}
        mock_resp.links = links or {}

        # Setup the async context manager
        mock_context = AsyncMock()
        mock_context.__aenter__.return_value = mock_resp
        return mock_context

    async def test_get_issue_count_success(self) -> None:
        """Test that issue count correctly parses the total_count from GitHub."""
        mock_context = self._create_mock_response(json_data={"total_count": 42})
        self.bot.http_session.get.return_value = mock_context

        result = await self.cog.get_issue_count("python-discord/bot", "2023-01-01", "2023-12-31", "created")
        self.assertEqual(result, 42)

    async def test_get_pr_count_merged(self) -> None:
        """Test that PR count handles the merged action."""
        mock_context = self._create_mock_response(json_data={"total_count": 15})
        self.bot.http_session.get.return_value = mock_context

        result = await self.cog.get_pr_count("python-discord/bot", "2023-01-01", "2023-12-31", "merged")
        self.assertEqual(result, 15)

    async def test_get_commit_count_multiple_pages(self) -> None:
        """Test that commit count parses the Link header using regex."""
        # Simulated regex match for the last page
        mock_headers = {"Link": '<https://api.github.com/repositories/123/commits?page=88>; rel="last"'}
        mock_context = self._create_mock_response(json_data=[{"commit": "data"}], headers=mock_headers)
        self.bot.http_session.get.return_value = mock_context

        result = await self.cog.get_commit_count("python-discord/bot", "2023-01-01", "2023-12-31")
        self.assertEqual(result, 88)

    async def test_api_failure_returns_negative_one(self) -> None:
        """Test that a 404 or 403 error safely returns -1 to prevent crashes."""
        mock_context = self._create_mock_response(status=404)
        self.bot.http_session.get.return_value = mock_context

        result = await self.cog.get_issue_count("invalid/repo", "2023-01-01", "2023-12-31", "created")
        self.assertEqual(result, -1)

<<<<<<< HEAD
    async def test_validate_date_accepts_valid_formats(self) -> None:
        """Valid date strings should be accepted."""
        valid_date = "2025-04-01"
        self.assertTrue(self, self.cog.validate_date_format(valid_date))

    async def test_validate_date_range_accepts_correct_order(self) -> None:
        """The method should accept dates that are ordered correct."""
        result = self.cog.validate_date_range(
=======
class TestDateFormat(unittest.TestCase):
    """Tests for validate_date_format."""

    def test_validate_date_accepts_valid_formats(self) -> None:
        """Valid date strings should be accepted."""
        valid_date = "2025-04-01"
        self.assertTrue(GithubInfo.validate_date_format(valid_date))

    def test_validate_date_rejects_invalid_formats(self) -> None:
        """Invalid date formats should be rejected."""
        invalid_dates = (
            "2025/04/01", # Invalid separator
            "04-2025-01", # Wrong order
            "2025.04.01", # Invalid separator
            "2025-4-01", # Missing zero padding
            "2025-04-1", # Missing zero padding
            "2025-13-01", # Invalid month
            "2025-04-32", # Invalid day
            "2025-04.01", # Invalid separator
            "2025.04-01", # Invalid separator
            "cookie", # No date
            "", # Empty string
        )

        for date_str in invalid_dates:
            with self.subTest(date=date_str):
                result = GithubInfo.validate_date_format(date_str)
                self.assertFalse(result)
                
                
class TestsValidDates(unittest.TestCase):
    """Tests for validate_date_range."""

    def test_validate_date_range_accepts_correct_order(self) -> None:
        """The method should accept dates that are ordered correct."""
        result = GithubInfo.validate_date_range(
>>>>>>> 1641d55f7801668eecf8d9fc544ce605f428e410
            "2025-04-01",
            "2025-04-11",
        )
        self.assertTrue(result)

<<<<<<< HEAD
    async def test_validate_date_range_rejects_wrong_order(self) -> None:
        """The method should reject dates that are ordered wrong."""
        result = self.cog.validate_date_range(
            "2025-04-11",
            "2025-04-01",
        )

        self.assertFalse(result)

    async def test_validate_date_range_accepts_same_day(self) -> None:
        """The method should accept the same dates."""
        result = self.cog.validate_date_range(
            "2025-04-01",
            "2025-04-01",
        )

=======
    def test_validate_date_range_rejects_wrong_order(self) -> None:
        """The method should reject dates that are ordered wrong."""
        result = GithubInfo.validate_date_range(
            "2025-04-11",
            "2025-04-01",
        )
        self.assertFalse(result)

    def test_validate_date_range_accepts_same_day(self) -> None:
        """The method should accept the same dates."""
        result = GithubInfo.validate_date_range(
            "2025-04-01",
            "2025-04-01",
        )
>>>>>>> 1641d55f7801668eecf8d9fc544ce605f428e410
        self.assertTrue(result)
