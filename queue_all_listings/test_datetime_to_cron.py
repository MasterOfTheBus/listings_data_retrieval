import unittest
from datetime import datetime
from index import datetime_to_cron


class TestDatetimeToCron(unittest.TestCase):
    def test_should_not_ignore_row(self):
        # year, month, day, hour, minute, second
        test_time = datetime(2002, 12, 4, 20, 30, 40)
        # Minutes Hours DayOfMonth Month DayOfWeek Year
        self.assertEqual(datetime_to_cron(test_time), '30 20 04 12 ? 2002')


if __name__ == '__main__':
    unittest.main()
