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


def median_of_sorted_lists_slow(a: list[float], b: list[float]) -> float:
    """Given two sorted lists of numbers, return the median in O(n log n) time."""
    assert is_monotonic(a)
    assert is_monotonic(b)
    return median_sorted(sorted(a + b))


def median_of_sorted_lists(a: list[float], b: list[float]) -> float:
    """Given two sorted lists of numbers, return the median in O(log n) time."""
    # assert is_monotonic(a)
    # assert is_monotonic(b)
    n = len(a) + len(b)
    if n % 2 == 0:
        return (kth(a, b, n // 2 - 1) + kth(a, b, n // 2)) / 2
    return kth(a, b, n // 2)


def kth(a: list[float], b: list[float], k: int) -> float:  # noqa PLR0911
    """Return the kth element of two sorted lists, in O(log n) time."""
    if not a:
        return b[k]
    if not b:
        return a[k]
    if k == 0:
        return min(a[0], b[0])

    # binary search
    ia, ib = len(a) // 2, len(b) // 2
    if ia + ib < k:
        if a[ia] > b[ib]:
            return kth(a, b[ib + 1 :], k - ib - 1)
        return kth(a[ia + 1 :], b, k - ia - 1)
    if a[ia] > b[ib]:
        return kth(a[:ia], b, k)
    return kth(a, b[:ib], k)


class MedianTest(unittest.TestCase):
    def test_median_of_sorted_lists_slow(self) -> None:
        median_two = median_of_sorted_lists  # _slow
        self.assertEqual(median_two([1, 3], [2]), 2)
        self.assertEqual(median_two([1, 2], [3, 4]), 2.5)
        self.assertEqual(median_two([0, 0], [0, 0]), 0)
        self.assertEqual(median_two([], [1]), 1)
        self.assertEqual(median_two([2], []), 2)

    def test_is_monotonic(self) -> None:
        self.assertTrue(is_monotonic([1, 1, 1, 1, 1, 1, 1]))
        self.assertTrue(is_monotonic([1, 1, 2, 2, 3, 4, 4]))
        self.assertTrue(is_monotonic([1, 2, 3, 4, 5, 6, 7]))

    def test_median(self) -> None:
        median = median_general
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([3, 1, 2, 5, 3]), 3)
        self.assertEqual(median([1, 300, 2, 200, 1]), 2)
        self.assertEqual(median([3, 6, 20, 99, 10, 15]), 12.5)
