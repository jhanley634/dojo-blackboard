def find_two_sum_quadratic(arr: list[int], target: int) -> tuple[int, int]:
    """
    Finds the two numbers that sum to a target number.

    We are guaranteed a unique solution;
    exactly two of the inputs will sum to the desired target.

    The naïve solution has O(n^2) quadratic complexity.
    """
    for x in arr:
        for y in arr:
            if x + y == target:
                return (x, y)

    diagnostic = f"The input arr must contain a pair which sums to {target}"
    raise ValueError(diagnostic)
