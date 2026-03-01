import unittest

from bot.exts.utilities.githubinfo import validate_date_range


class TestsValidDates(unittest.TestCase):
    """Tests for validate_date_range."""

    def test_validate_date_range_accepts_correct_order(self) -> None:
        """The method should accept dates that are ordered correct."""
        result = validate_date_range(
            "2025-04-01",
            "2025-04-11",
        )
        self.assertTrue(result)

    def test_validate_date_range_rejects_wrong_order(self) -> None:
        """The method should reject dates that are ordered wrong."""
        result = validate_date_range(
            "2025-04-11",
            "2025-04-01",
        )
        self.assertFalse(result)

    def test_validate_date_range_accepts_same_day(self) -> None:
        """The method should accept the same dates."""
        result = validate_date_range(
            "2025-04-01",
            "2025-04-01",
        )
        self.assertTrue(result)
