import unittest
from index import should_ignore_row


class TestDateComparison(unittest.TestCase):

    def test_should_ignore_row(self):
        test_name_TEST = {"symbol": "ZVV", "name": "LISTED TEST SYMBOL"}
        test_name_Unit = {"symbol": "AACU",
                          "name": "Ares Corporation - "
                          "Units (1 Ord Share Class A & 1/5 War)"}
        test_name_Warrants = {"symbol": "ACQRW",
                              "name": "Independence Holdings Corp - "
                              "Warrants (31/03/2028)"}
        test_name_Acquisition = {"symbol": "AAC",
                                 "name": "Ares Acquisition Corporation -"
                                 " Class A"}
        test_symbol_dash = {"symbol": "AAC-U", "name": "Ares  Corporation"}
        self.assertEqual(should_ignore_row(test_name_TEST), True)
        self.assertEqual(should_ignore_row(test_name_Unit), True)
        self.assertEqual(should_ignore_row(test_name_Warrants), True)
        self.assertEqual(should_ignore_row(test_name_Acquisition), True)
        self.assertEqual(should_ignore_row(test_symbol_dash), True)

        test_do_not_ignore = {"symbol": "ACON", "name": "Aclarion Inc"}
        self.assertEqual(should_ignore_row(test_do_not_ignore), False)


if __name__ == '__main__':
    unittest.main()
