import unittest
from index import create_records, get_list_of_symbols, read_file_data


class TestCreateRecords(unittest.TestCase):

    def test_create_records_from_file(self):
        with open('test.csv', 'rb') as f:
            data = {'Body': f}
            data = read_file_data(data)
            symbols = get_list_of_symbols(data)
            self.assertSequenceEqual(symbols, [
                {'symbol': 'A', 'next': 'AA'},
                {'symbol': 'AA', 'next': 'AACG'},
                {'symbol': 'AACG', 'next': 'AADI'},
                {'symbol': 'AADI', 'next': ''}
            ])

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
            'symbol,name,NYSE,Stock',
            'AA,AA Company,NYSE,Stock',
            'AACU,Ares Corporation - Units (1 Ord Share Class A & 1/5 War)\
                ,NYSE,Stock',
            'BB,BB Company,NYSE,Stock',
            'CC-U,CC Company,NYSE,Stock'
        ]
        symbols = get_list_of_symbols(rows_data=rows)
        self.assertSequenceEqual(symbols, [
            {'symbol': 'AA', 'next': 'BB'},
            {'symbol': 'BB', 'next': ''},
        ])


if __name__ == '__main__':
    unittest.main()
