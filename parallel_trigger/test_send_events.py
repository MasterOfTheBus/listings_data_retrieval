import unittest
from index import send_events


class MockSns:
    def publish(self, TopicArn, Message):
        pass


class TestIgnoreRow(unittest.TestCase):

    def test_send_events_more_symbols(self):
        mock = MockSns()
        remaining = send_events(
            sns=mock, symbols=['a', 'b', 'c'], topic='', num_parallel=2
        )
        self.assertEqual(remaining, ['c'])

    def test_send_events_more_parallel(self):
        mock = MockSns()
        remaining = send_events(
            sns=mock, symbols=['a'], topic='', num_parallel=2
        )
        self.assertEqual(remaining, [])


if __name__ == '__main__':
    unittest.main()
