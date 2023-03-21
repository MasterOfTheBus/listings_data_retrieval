import unittest
from datetime import date, timedelta
from index import current_day_before_or_equals_saved_date


class TestDateComparison(unittest.TestCase):

    def test_current_day_before_stored_date(self):
        day = date.today() + timedelta(days=10)
        result = current_day_before_or_equals_saved_date(day.isoformat())
        self.assertEqual(result, True)

    def test_current_day_after_stored_date(self):
        day = date.today() - timedelta(days=10)
        result = current_day_before_or_equals_saved_date(day.isoformat())
        self.assertEqual(result, False)

    def test_current_day_equals_stored_date(self):
        day = date.today()
        result = current_day_before_or_equals_saved_date(day.isoformat())
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
