import unittest
import csv
from datetime import timedelta
from index import map_symbol_to_date


class TestRowMapping(unittest.TestCase):
    mapping_result = dict()

    def handler(self, symbol, day_time):
        self.mapping_result[symbol] = day_time

    def test_map_rows_small_set(self):
        self.mapping_result = dict()
        test_data = []
        with open('small_set.csv', 'r') as file:
            test_data = [line for line in file]

        map_symbol_to_date(row_data=test_data,
                           daily_limit=10,
                           minute_limit=5,
                           mapping_handler=self.handler)

        # Expect 2 per day
        self.assertEqual(len(self.mapping_result), 5)
        self.assertIn('FTAI', self.mapping_result)
        self.assertIn('FTCH', self.mapping_result)
        self.assertIn('FTCI', self.mapping_result)
        self.assertIn('FTDR', self.mapping_result)
        self.assertIn('FTEK', self.mapping_result)

        first = self.mapping_result['FTAI']
        second = self.mapping_result['FTCH']
        third = self.mapping_result['FTCI']
        fourth = self.mapping_result['FTDR']
        fifth = self.mapping_result['FTEK']
        self.assertEqual(first + timedelta(minutes=1), second)
        self.assertEqual(second + timedelta(days=1), third)
        self.assertEqual(third + timedelta(minutes=1), fourth)
        self.assertEqual(fourth + timedelta(days=1), fifth)

    def test_map_rows_full_set(self):
        self.mapping_result = dict()
        test_data = []
        with open('full_set.csv', 'r') as file:
            for line in file:
                test_data.append(line)

        map_symbol_to_date(row_data=test_data,
                           daily_limit=500,
                           minute_limit=5,
                           mapping_handler=self.handler)

        with open('full_set_results.csv', 'w') as csvfile:
            fieldnames = ['symbol', 'datetime']
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
            for k, v in self.mapping_result.items():
                writer.writerow({'symbol': k, 'datetime': v.isoformat()})


if __name__ == '__main__':
    unittest.main()
