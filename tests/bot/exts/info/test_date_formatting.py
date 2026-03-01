import unittest

from bot.exts.utilities.githubinfo import validate_date_format

# Date formats: YYYY-MM-DD, DD-MM-YYYY, MM-DD-YYYY
# The test tests if the date format is valid
# Method name could be:
# async def validate_date_format(self, date_str: str) -> bool:
# This method should test the given string if its formatted correctly

class TestDateFormat(unittest.TestCase):
    """Tests for validate_date_format."""

    def test_validate_date_accepts_valid_formats(self) -> None:
        """Valid date strings should be accepted."""
        valid_date = "2025-04-01"
        self.assertTrue(validate_date_format(valid_date))

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
                result = validate_date_format(date_str)
                self.assertFalse(result)
