import unittest

# from bot.exts.info import github_stats
from tests.helpers import MockBot, MockContext


# async def validate_date_range(self, start_date: str, end_date: str) -> bool:
# This method should control that the given dates are in the correct order meaning start_date <= end_date.
class GitStatsCogTestsValidDates(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Attach an instance of the cog to the class for tests."""
        self.bot = MockBot()
        # self.cog = github_stats.Stats(self.bot)
        self.ctx = MockContext(bot=self.bot)

    async def test_validate_date_range_accepts_correct_order(self):
        """The method should accept dates that are ordered correct"""
        result = await self.cog.validate_date_range(
            "2025-04-01",
            "2025-04-11",
        )
        self.assertTrue(result)

    async def test_validate_date_range_rejects_wrong_order(self):
        """The method should reject dates that are ordered wrong"""
        result = await self.cog.validate_date_range(
            "2025-04-11",
            "2025-04-01",
        )
        self.assertFalse(result)
