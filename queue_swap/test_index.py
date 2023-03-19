import unittest
from index import calc_iterations


class TestMessageHandling(unittest.TestCase):

    def test_calc_iterations_greater_than_max(self):
        response = calc_iterations(60, 900, 20)
        self.assertEqual(response, 40)

    def test_calc_iterations_less_than_max(self):
        response = calc_iterations(30, 900, 20)
        self.assertEqual(response, 30)

    def test_calc_iterations_equal_max(self):
        response = calc_iterations(40, 900, 20)
        self.assertEqual(response, 40)


if __name__ == '__main__':
    unittest.main()
