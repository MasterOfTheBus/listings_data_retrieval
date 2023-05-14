import unittest
from index import get_list_of_symbols, read_file_data


class TestCreateRecords(unittest.TestCase):

    def test_create_records_from_file(self):
        with open('test.csv', 'rb') as f:
            data = {'Body': f}
            data = read_file_data(data)
            symbols = get_list_of_symbols(data)
            self.assertSequenceEqual(symbols, [
                'A', 'AA', 'AACG', 'AADI'
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
            'AA', 'BB'
        ])


if __name__ == '__main__':
    unittest.main()
