import unittest
from typing import Self


class SlicedList:
    """Models a slice of a list using start and end index, with zero copies."""

    def __init__(self, nums: list[float]) -> None:
        self.nums = nums
        self.start = 0
        self.end = len(nums)

    def slice(self, start: int, end: int | None = None) -> Self:
        length = self.end - self.start
        end_i: int = length if end is None else end
        assert 0 <= start <= end_i <= length

        self.end = self.start + end_i
        self.start += start
        assert self.start <= self.end
        return self

    def __getitem__(self, i: int) -> float:
        return self.nums[self.start + i]

    def __len__(self) -> int:
        return self.end - self.start

    def __str__(self) -> str:
        return str(self.nums[self.start : self.end])


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


def median_of_sorted_lists(a_in: list[float], b_in: list[float]) -> float:
    """Given two sorted lists of numbers, return the median in O(log n) time."""
    # assert is_monotonic(a_in)
    # assert is_monotonic(b_in)
    n = len(a_in) + len(b_in)
    a = SlicedList(a_in)
    b = SlicedList(b_in)
    if n % 2 == 0:
        return (kth(a, b, n // 2 - 1) + kth(a, b, n // 2)) / 2
    return kth(a, b, n // 2)


def kth(a: SlicedList, b: SlicedList, k: int) -> float:  # noqa PLR0911
    """Return the kth element of two sorted lists, in O(log n) time."""
    assert 0 <= k < len(a) + len(b), f"{k}, {a}, {b}"
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
            return kth(a, SlicedList(b.nums[ib + 1 :]), k - ib - 1)
        return kth(SlicedList(a.nums[ia + 1 :]), b, k - ia - 1)
    if a[ia] > b[ib]:
        return kth(a.slice(0, ia), b, k)
    return kth(a, SlicedList(b.nums[:ib]), k)


class MedianTest(unittest.TestCase):

    def test_sliced_list(self) -> None:
        a = SlicedList([0, 1, 2, 3, 4])
        self.assertEqual(5, len(a))
        self.assertEqual(4, len(a.slice(1)))
        self.assertEqual(4, len(a))
        self.assertEqual(2, a[1])
        self.assertEqual(3, a[2])

        a.slice(0, 4)
        self.assertEqual(4, len(a))
        a.slice(0, 3)
        self.assertEqual(3, len(a))
        self.assertEqual(3, a[2])
        self.assertEqual([0, 1, 2, 3, 4], a.nums)

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

    def test_median_of_sorted_lists_slow(self) -> None:
        median_two = median_of_sorted_lists  # _slow
        self.assertEqual(median_two([], [1]), 1)
        self.assertEqual(median_two([2], []), 2)
        self.assertEqual(median_two([1, 3], [2]), 2)
        self.assertEqual(median_two([0, 0], [0, 0]), 0)
        self.assertEqual(median_two([1, 2], [3, 4]), 2.5)
