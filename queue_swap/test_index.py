import unittest
from datetime import datetime, timedelta
from index import handle_batch


class TestMessageHandling(unittest.TestCase):

    epoch = datetime.utcfromtimestamp(0)

    def test_some_newer_messages(self):
        def receive(): return [self.create_message(15, 'a'),
                               self.create_message(13, 'b'),
                               self.create_message(9, 'c')]

        def send(entries):
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]['MessageBody'], 'a')
            self.assertEqual(entries[1]['MessageBody'], 'b')

        should_continue = handle_batch(receive, send, 13)
        self.assertEqual(should_continue, False)

    def test_all_old_messages(self):
        def receive(): return [self.create_message(15, 'a'),
                               self.create_message(14, 'b'),
                               self.create_message(13, 'c')]

        def send(entries):
            self.assertEqual(len(entries), 3)
            self.assertEqual(entries[0]['MessageBody'], 'a')
            self.assertEqual(entries[1]['MessageBody'], 'b')
            self.assertEqual(entries[2]['MessageBody'], 'c')

        should_continue = handle_batch(receive, send, 13)
        self.assertEqual(should_continue, True)

    def test_all_new_messages(self):
        def receive(): return [self.create_message(12, 'a'),
                               self.create_message(11, 'b'),
                               self.create_message(10, 'c')]

        def send(entries):
            self.assertEqual(entries, None)

        should_continue = handle_batch(receive, send, 13)
        self.assertEqual(should_continue, False)

    def test_empty(self):
        def receive(): return []

        def send(entries):
            self.assertEqual(entries, None)

        should_continue = handle_batch(receive, send, 13)
        self.assertEqual(should_continue, False)

    def create_message(self, day_delta, body):
        timestamp = datetime.today() - timedelta(days=day_delta)
        ms = int((timestamp - self.epoch).total_seconds() * 1000)
        return {'Body': body, 'Attributes': {'SentTimestamp': str(ms)}}


if __name__ == '__main__':
    unittest.main()
