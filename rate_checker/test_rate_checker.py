import unittest
from datetime import date, timedelta, datetime
from index import current_day_before_or_equals_saved_date, \
    calc_wait_until_next_day


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
        expected_day = datetime(year=2023, month=4, day=2,
                                hour=12, minute=0, second=0)

        next_day = calc_wait_until_next_day(test_day)
        self.assertEqual(next_day, expected_day)


if __name__ == '__main__':
    unittest.main()
