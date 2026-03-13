"""
Finds the two numbers x + y that sum to a target number.

We are guaranteed a unique solution;
exactly two of the inputs will sum to the desired target.
"""

from sortedcontainers import SortedList


class InputArrayError(ValueError):
    def __init__(self, target: int) -> None:
        super().__init__(f"The input array must contain a pair which sums to {target}")


def ordered(x: int, y: int) -> tuple[int, int]:
    """
    Sorts a pair of integers.

    Addition is commutative, and the original
    problem imposed no requirement on whether
    we answer with (x, y) or with (y, x).
    Requiring an answer with x <= y makes it
    convenient for the test driver to compare
    answers across diverse implementations.

    Or, the problem might have asked for set([x, y]).
    I'm just conforming to its specified tuple signature.
    """
    return (x, y) if x < y else (y, x)


def find_two_sum(arr: list[int], target: int) -> tuple[int, int]:
    xs = SortedList(arr)
    for y in (target - x for x in xs):  # O(n) linear cost
        # Binary search for the `in` probe has O(log n) cost.
        if y in xs:
            return ordered(target - y, y)

    # total cost: O(n log n)

    raise InputArrayError(target)


def find_two_sum_naive(arr: list[int], target: int) -> tuple[int, int]:

    # The naïve solution has O(n^2) quadratic complexity,
    # as each of the nested loops has O(n) linear cost.
    #
    # Also, this solution is only partly correct.
    # Consider [3, 5, 1] with target 6.
    # If .5 * target is present in `arr`, we
    # incorrectly report it, e.g. (3, 3).

    for x in arr:
        for y in arr:
            if x + y == target:
                return ordered(x, y)

    raise InputArrayError(target)

    # We could slightly reduce the cost
    # from n² down to ½ n² but that is still O(n^2).
    # If we go that route, then the following
    # is _not_ the way to do it.
    #
    #   for i, x in enumerate(arr):
    #       for y in arr[i+1:]:
    #
    # Why is that bad? Because the [i+1:] slicing
    # operation creates a smaller copy of the list,
    # roughly doubling the work we do.
    # Prefer to use enumerate(), range(), and indexing
    # of arr[j] if you really want the 50% savings.
    # OTOH numpy slicing _is_ efficient in the hoped for way.


def find_two_sum_quadratic(arr: list[int], target: int) -> tuple[int, int]:
    for i, x in enumerate(arr):
        for j, y in enumerate(arr):
            if i != j and x + y == target:
                return ordered(x, y)

    # total cost: O(n^2) quadratic

    raise InputArrayError(target)


def find_two_sum_with_set(arr: list[int], target: int) -> tuple[int, int]:
    seen = set()
    for x in arr:  # O(n) linear
        y = target - x
        if y in seen:  # O(1) constant lookup time
            return ordered(x, y)
        seen.add(x)

    # total cost: O(n) linear

    raise InputArrayError(target)
