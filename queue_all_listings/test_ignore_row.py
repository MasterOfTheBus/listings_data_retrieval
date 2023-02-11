import unittest
from index import should_ignore_row


class TestDateComparison(unittest.TestCase):

    def test_should_ignore_row(self):
        self.assertEqual(should_ignore_row(
            symbol='ZVV', name='LISTED TEST SYMBOL', type='STOCK'
        ), True)
        self.assertEqual(should_ignore_row(
            symbol='AACU',
            name='Ares Corporation - Units (1 Ord Share Class A & 1/5 War)',
            type='STOCK'
        ), True)
        self.assertEqual(should_ignore_row(
            symbol='ACQRW',
            name="Independence Holdings Corp - Warrants (31/03/2028)",
            type='STOCK'
        ), True)
        self.assertEqual(should_ignore_row(
            symbol='AAC', name='Ares Acquisition Corporation - Class A',
            type='STOCK'
        ), True)
        self.assertEqual(should_ignore_row(
            symbol='AAC-U', name='Ares  Corporation', type='STOCK'
        ), True)
        self.assertEqual(should_ignore_row(
            symbol='AACETF', name='An ETF', type='ETF'
        ), True)

    def test_should_not_ignore_row(self):
        self.assertEqual(should_ignore_row(
            symbol='ACON', name='Aclarion Inc', type='STOCK'
        ), False)


if __name__ == '__main__':
    unittest.main()
