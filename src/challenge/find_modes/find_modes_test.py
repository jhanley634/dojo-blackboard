import unittest
from pathlib import Path

import numpy as np
import pandas as pd


def fetch_input_data(n: int) -> list[int]:
    data_dir = Path("src/challenge/find_modes/data")
    assert data_dir.exists()

    csv = data_dir / f"{n}_random_numbers.txt"
    if csv.exists():
        df = pd.read_csv(csv, header=None, names=["n"])
        return df.n.to_list()

    rng = np.random.default_rng()
    return list(rng.integers(0, 1000, size=1_000_000, dtype=np.int32))


class FindModesTest(unittest.TestCase):

    def test_fetch(self) -> None:
        xs = fetch_input_data(1001)
        print(xs)
