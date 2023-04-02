import unittest
import json


class TestStateMachine(unittest.TestCase):

    def get_execution_history(self):
        with open('execution_results.json', 'r') as f:
            execution_history = json.load(f)
            return execution_history['events']

    def test_happy_path(self):
        events = self.get_execution_history()

        no_failures = True
        failures = []
        for event in events:
            event_success = event['type'] != 'ExecutionFailed'
            no_failures = no_failures and event_success
            if not event_success:
                failures.append(event)

        if not no_failures:
            print('\n=== Failures in State Machine ===\n')
            print(failures)
        self.assertTrue(no_failures)

    def test_events_order(self):
        events = self.get_execution_history()

        event_order = [
            # Startup
            'Ignore Queue All Listings',
            'Queue All Listings',
            # Initial Loop
            'Rate Checker',
            'Daily Rate Reached',
            'Get Listing Info',
            'Queue Empty',
            'Wait 1 Minute',
            # Wait Loop
            'Rate Checker',
            'Daily Rate Reached',
            'Wait Until Next Day',
            # Last Loop
            'Rate Checker',
            'Daily Rate Reached',
            'Get Listing Info',
            'Queue Empty',
            'Go To end',
        ]

        exited_states = []
        for event in events:
            if 'StateExited' in event['type']:
                name = event['stateExitedEventDetails']['name']
                exited_states.append(name)

        self.assertEqual(len(event_order), len(exited_states))
        for i in range(len(exited_states)):
            self.assertEqual(exited_states[i], event_order[i])


if __name__ == '__main__':
    unittest.main()
