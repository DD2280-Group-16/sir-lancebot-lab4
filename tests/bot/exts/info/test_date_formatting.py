import unittest

# from bot.exts.info import github_stats
from tests.helpers import MockBot, MockContext

# Date formats: YYYY-MM-DD, DD-MM-YYYY, MM-DD-YYYY
# The test tests if the date format is valid
# Method name could be:
# async def validate_date_format(self, date_str: str) -> bool:
# This method should test the given string if its formatted correctly

class GitStatsCogTestDateFormat(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """Attach an instance of the cog to the class for tests."""
        self.bot = MockBot()
        # self.cog = github_stats.Stats(self.bot)
        self.ctx = MockContext(bot=self.bot)

    async def test_validate_date_accepts_valid_formats(self):
        """Valid date strings should be accepted"""
        valid_dates = (
            "2025-04-01", # YYYY-MM-DD ISO Standard
            "01-04-2025", # DD-MM-YYYY Europe/UK
            "04-01-2025", # MM-DD-YYYY US
        )

        for date_str in valid_dates:
            with self.subTest(date=date_str):
                    result = await self.cog.validate_date_format(date_str)
                    self.assertTrue(result)

    # Some of the invalid dates might be able to be checked on the github
    # side of things.
    async def test_validate_date_rejects_invalid_formats(self):
        """Invalid date formats should be rejected"""
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
            with self.subTest(date_str):
                result = await self.cog.validate_date_format(date_str)
                self.assertFalse(result)
