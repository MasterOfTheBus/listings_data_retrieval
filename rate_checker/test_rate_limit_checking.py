import unittest
from datetime import date, timedelta
from index import check_rate_limit


class TestRateChecking(unittest.TestCase):

    reset_called = False

    def mock_reset(self, ddb, table):
        self.reset_called = True

    def test_count_less_than_daily_limit(self):
        day = date.today()
        result = check_rate_limit(count=5, daily_limit=10, day=day.isoformat(),
                                  reset_rate=self.mock_reset,
                                  ddb=None, table=None)
        self.assertFalse(result['wait'])
        self.assertFalse(self.reset_called)

    def test_count_at_daily_limit_at_stored_date(self):
        day = date.today()
        result = check_rate_limit(count=10, daily_limit=10,
                                  day=day.isoformat(),
                                  reset_rate=self.mock_reset,
                                  ddb=None, table=None)
        self.assertTrue(result['wait'])
        next_day = day + timedelta(days=1)
        next_day_str = next_day.isoformat() + "T00:00:00Z"
        self.assertEqual(result['next_day'], next_day_str)
        self.assertFalse(self.reset_called)

    def test_count_at_daily_limit_past_stored_date(self):
        day = date.today() - timedelta(days=1)
        result = check_rate_limit(count=10, daily_limit=10,
                                  day=day.isoformat(),
                                  reset_rate=self.mock_reset,
                                  ddb=None, table=None)
        self.assertFalse(result['wait'])
        self.assertTrue(self.reset_called)
        self.reset_called = False


if __name__ == '__main__':
    unittest.main()
