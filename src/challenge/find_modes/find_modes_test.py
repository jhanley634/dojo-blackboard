import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray


def fetch_input_data(n: int) -> NDArray[np.int32]:
    data_dir = Path("src/challenge/find_modes/data")
    assert data_dir.exists()

    csv = data_dir / f"{n:,}_random_numbers.txt".replace(",", "_")
    if csv.exists():
        df = pd.read_csv(csv, header=None, names=["n"])
        return np.array(df.n.astype(np.int32).to_numpy())

    rng = np.random.default_rng(seed=42)
    return rng.integers(0, 1_000, size=1_000_000, dtype=np.int32)


class FindModesTest(unittest.TestCase):

    def test_fetch(self) -> None:
        xs = fetch_input_data(10_000)
        xs = fetch_input_data(100)
        xs = fetch_input_data(200)
        for x in xs:
            assert 0 <= x < 1_000
