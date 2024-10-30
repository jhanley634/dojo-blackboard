import unittest


def median_general(nums: list[float]) -> float:
    return median_sorted(sorted(nums))


def is_monotonic(nums: list[float]) -> bool:
    return all(a <= b for a, b in zip(nums, nums[1:]))


def median_sorted(nums: list[float]) -> float:
    """Given a sorted list of numbers, return the median in O(1) constant time."""
    # assert is_monotonic(nums), "Input must already be sorted."
    n = len(nums)
    if n % 2 == 0:
        return (nums[n // 2 - 1] + nums[n // 2]) / 2
    return nums[n // 2]


class MedianTest(unittest.TestCase):
    def test_is_monotonic(self) -> None:
        self.assertTrue(is_monotonic([1, 1, 1, 1, 1, 1, 1]))
        self.assertTrue(is_monotonic([1, 1, 2, 2, 3, 4, 4]))

    def test_median(self) -> None:
        median = median_general
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([3, 1, 2, 5, 3]), 3)
        self.assertEqual(median([1, 300, 2, 200, 1]), 2)
        self.assertEqual(median([3, 6, 20, 99, 10, 15]), 12.5)
