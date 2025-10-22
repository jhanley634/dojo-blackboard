from collections.abc import Generator

import numpy as np
from numpy.typing import NDArray


def find_modes_via_sorting(xs: NDArray[np.int32]) -> list[int]:
    xs.sort()

    max_n = 0
    for n, _ in get_runs(xs):
        max_n = max(n, max_n)

    return [value for n, value in get_runs(xs) if max_n == n]


def get_runs(xs: NDArray[np.int32]) -> Generator[tuple[int, int]]:
    """Generates a (count, value) tuple for each run of an observed value."""
    n = 0
    prev = xs[0]  # input shall be non-empty

    for x in xs:
        if x < prev:
            raise ValueError  # input must be monotonic increasing
        if x == prev:
            n += 1
        else:
            yield n, int(prev)
            n = 1
            prev = x

    yield n, int(prev)
