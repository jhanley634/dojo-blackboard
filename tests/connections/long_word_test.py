import unittest

import pandas as pd

from connections.conn_util import get_examples
from connections.long_word import find_longest_match, find_words


class LongWordTest(unittest.TestCase):

    def test_longest_match(self) -> None:
        pfx, word = find_longest_match("CUPSCAR")
        self.assertEqual("SCAR", word)
        self.assertEqual("CUP", pfx)

    def test_find_words(self) -> None:
        self.assertEqual(["CUP", "SCAR"], find_words("CUPSCAR"))

    def test_examples(self, *, verbose: bool = False) -> None:
        df = pd.DataFrame(get_examples())
        self.assertGreaterEqual(len(df), 1064)
        for row in df.itertuples():
            cat = f"{row.category}"
            assert isinstance(row.words, list)
            squished = "".join(row.words)  # type: ignore
            if verbose:
                print(cat.ljust(33), squished)
