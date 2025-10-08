import unittest

from challenge.two_sum.find_two_sum import find_two_sum_quadratic

arr = [7, 3, 5, 9]
target = 8


class FindTwoSumTest(unittest.TestCase):
    def test_quadratic(self) -> None:
        self.assertEqual(
            (3, 5),
            find_two_sum_quadratic(arr, target),
        )
