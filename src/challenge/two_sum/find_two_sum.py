from sortedcontainers import SortedList


def find_two_sum_quadratic(arr: list[int], target: int) -> tuple[int, int]:
    """
    Finds the two numbers x + y that sum to a target number.

    We are guaranteed a unique solution;
    exactly two of the inputs will sum to the desired target.

    The naïve solution has O(n^2) quadratic complexity.
    """
    for x in arr:
        for y in arr:
            if x + y == target:
                return x, y

    diagnostic = f"The input arr must contain a pair which sums to {target}"
    raise ValueError(diagnostic)


def find_two_sum(arr: list[int], target: int) -> tuple[int, int]:
    """
    Finds the two numbers x + y that sum to a target number.

    We are guaranteed a unique solution;
    exactly two of the inputs will sum to the desired target.

    A linear O(n) pass lets us complete the task in O(n log n) time.
    """
    xs = SortedList(arr)
    for y in (target - x for x in xs):
        if y in xs:
            return target - y, y

    diagnostic = f"The input arr must contain a pair which sums to {target}"
    raise ValueError(diagnostic)
