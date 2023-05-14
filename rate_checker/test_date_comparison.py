import unittest
from datetime import date, timedelta
from index import current_day_before_or_equals_saved_date, \
    calc_next_day_timestamp


class TestDateComparison(unittest.TestCase):

    # current_day_before_or_equals_saved_date Tests

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

    # calc_wait_until_next_day Tests

    def test_calc_wait_until_next_day(self):
        test_day = date(year=2023, month=4, day=1)
        next_day = calc_next_day_timestamp(test_day)
        self.assertEqual(next_day, "2023-04-02T00:00:00Z")


if __name__ == '__main__':
    unittest.main()
