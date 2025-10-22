from collections import Counter

import numpy as np
from numpy.typing import NDArray


def find_modes_via_counting(xs: NDArray[np.int16]) -> list[int]:
    assert len(xs) > 0

    c = Counter(map(int, xs))
    mode_count = sorted(c.values())[-1]
    return sorted(k for k, v in c.items() if v == mode_count)
