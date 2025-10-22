import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from challenge.find_modes.counting import find_modes_via_counting
from challenge.find_modes.sorting import find_modes_via_sorting, get_runs


def fetch_input_data(num_elts: int) -> NDArray[np.int16]:
    data_dir = Path("src/challenge/find_modes/data")
    assert data_dir.exists()

    csv = data_dir / f"{num_elts:,}_random_numbers.txt".replace(",", "_")
    if csv.exists():
        df = pd.read_csv(csv, header=None, names=["n"])
        return np.array(df.n.astype(np.int16).to_numpy())

    rng = np.random.default_rng(seed=42)
    return rng.integers(0, 1_000, size=num_elts, dtype=np.int16)


class FindModesTest(unittest.TestCase):

    def test_fetch(self) -> None:
        xs = fetch_input_data(10_000)
        xs = fetch_input_data(100)
        xs = fetch_input_data(200)
        for x in xs:
            assert 0 <= x < 1_000

    def test_get_runs(self) -> None:
        tests = [
            ([(1, 7)], [7]),
            ([(2, 7)], [7, 7]),
            ([(3, 7)], [7, 7, 7]),
            ([(1, 7), (1, 9)], [7, 9]),
            ([(1, 7), (2, 9)], [7, 9, 9]),
            ([(1, 7), (3, 8), (2, 9)], [7, 8, 8, 8, 9, 9]),
        ]
        for expected, xs in tests:
            self.assertEqual(
                expected,
                list(get_runs(np.array(xs))),
            )

        xs = [2, 3, 4, 99, 5, 6, 7]
        with self.assertRaises(ValueError):
            list(get_runs(np.array(xs)))

    # The "100" result is easily verified with this bash pipeline:
    # sort -n src/challenge/find_modes/data/100_random_numbers.txt |
    #   uniq -c | awk '$1 > 1'

    tests = (
        (100, [188, 208, 374, 546, 641, 694]),
        (1_000, [458, 804]),
        (10_000, [284]),
        (1_000_000, [25]),
        (10_000_000, [221]),
        # (100_000_000, [422]),  # This runs fine, slowly, in ~ 12 seconds.
    )

    def test_sorting(self) -> None:
        for n, modes in self.tests:
            self.assertEqual(modes, find_modes_via_sorting(fetch_input_data(n)))

    def test_counting(self) -> None:
        for n, modes in self.tests:
            self.assertEqual(modes, find_modes_via_counting(fetch_input_data(n)))
