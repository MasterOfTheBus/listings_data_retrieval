import unittest
from datetime import date, timedelta
from index import determine_wait


class TestRateChecker(unittest.TestCase):

    def test_count_less_than_all_limits_1(self):
        day = date.today()
        result = determine_wait(count=0, key=1, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 1)
        self.assertEqual(result['reset_db'], False)

    def test_count_less_than_all_limits_2(self):
        day = date.today()
        result = determine_wait(count=5, key=1, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 1)
        self.assertEqual(result['reset_db'], False)

    def test_count_equals_key_limit(self):
        day = date.today()
        result = determine_wait(count=10, key=1, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 2)
        self.assertEqual(result['reset_db'], False)

    def test_count_greater_than_key_limit_1(self):
        day = date.today()
        result = determine_wait(count=15, key=2, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 2)
        self.assertEqual(result['reset_db'], False)

    def test_count_greater_than_key_limit_2(self):
        day = date.today()
        result = determine_wait(count=25, key=3, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 3)
        self.assertEqual(result['reset_db'], False)

    def test_count_ge_day_limit_before_EOD(self):
        day = date.today()
        result = determine_wait(count=30, key=3, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], True)
        self.assertEqual(result['key'], 1)
        self.assertEqual(result['reset_db'], False)
        self.assertIsNotNone(result['next_day'])

    def test_count_ge_day_limit_next_day(self):
        day = date.today() - timedelta(days=1)
        result = determine_wait(count=30, key=3, day=day.isoformat(),
                                key_limit=10, num_keys=3)
        self.assertEqual(result['wait'], False)
        self.assertEqual(result['key'], 1)
        self.assertEqual(result['reset_db'], True)


if __name__ == '__main__':
    unittest.main()
