import unittest
from index import create_records, get_list_of_symbols


class TestCreateRecords(unittest.TestCase):

    def test_create_records(self):
        symbols = ['A', 'B', 'C', 'D', 'E']
        records = create_records(symbols)
        self.assertSequenceEqual(records, [
            {'symbol': 'A', 'next': 'B'},
            {'symbol': 'B', 'next': 'C'},
            {'symbol': 'C', 'next': 'D'},
            {'symbol': 'D', 'next': 'E'},
            {'symbol': 'E', 'next': ''}
        ])

    def test_get_list_of_symbols(self):
        rows = [
            'symbol,name',
            'AA,AA Company',
            'AACU,Ares Corporation - Units (1 Ord Share Class A & 1/5 War)',
            'BB,BB Company',
            'CC-U,CC Company'
        ]
        symbols = get_list_of_symbols(rows_data=rows)
        self.assertSequenceEqual(symbols, [
            {'symbol': 'AA', 'next': 'BB'},
            {'symbol': 'BB', 'next': ''},
        ])


if __name__ == '__main__':
    unittest.main()
