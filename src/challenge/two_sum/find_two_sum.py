from sortedcontainers import SortedList


class InputArrayError(ValueError):
    def __init__(self, target: int) -> None:
        super().__init__(f"The input arr must contain a pair which sums to {target}")


def ordered(x: int, y: int) -> tuple[int, int]:
    if x > y:
        x, y = y, x
    return x, y


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
                return ordered(x, y)

    raise InputArrayError(target)


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
            return ordered(target - y, y)

    raise InputArrayError(target)


def find_two_sum_with_set(arr: list[int], target: int) -> tuple[int, int]:
    """
    Finds the two numbers x + y that sum to a target number.

    We are guaranteed a unique solution;
    exactly two of the inputs will sum to the desired target.

    Using a set moves us from O(log n) lookups to O(1) lookups.
    Total cost is O(n) linear.
    """
    seen = set()
    for x in arr:
        y = target - x
        if y in seen:
            return ordered(x, y)
        seen.add(x)

    raise InputArrayError(target)
