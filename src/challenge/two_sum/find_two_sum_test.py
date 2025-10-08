import unittest

from challenge.two_sum.find_two_sum import (
    InputArrayError,
    find_two_sum,
    find_two_sum_quadratic,
    find_two_sum_with_set,
)

fns = [
    find_two_sum,
    find_two_sum_quadratic,
    find_two_sum_with_set,
]

arr = [7, 3, 5, 9]
target = 8


class FindTwoSumTest(unittest.TestCase):

    def test_find_two_sum(self) -> None:
        for fn in fns:
            self.assertEqual(
                (3, 5),
                fn(arr, target),
            )

    def test_impossible_problem(self) -> None:
        bad_target = 20  # infeasible
        for fn in fns:
            with self.assertRaises(InputArrayError):
                fn(arr, bad_target)
