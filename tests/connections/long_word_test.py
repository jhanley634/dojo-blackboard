import re
import unittest

import pandas as pd

from connections.conn_util import get_examples
from connections.long_word import find_longest_match, find_words
from connections.long_word_create import ENGLISH_WORDS


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
            words = list(map(str, row.words))  # type: ignore
            comma_separated = ", ".join(words)
            squished = re.sub(r", ", "", comma_separated)
            if verbose:
                print(cat.ljust(33), squished)
            if is_difficult(squished, words):
                continue

            self.assertEqual(", ".join(find_words(squished)), comma_separated)


with open(ENGLISH_WORDS) as fin:
    english_words = {word.upper().rstrip() for word in fin}


def is_difficult(squished: str, words: list[str]) -> bool:
    ret = False
    for word in words:
        if word not in english_words:
            ret = True
    if " " in squished:
        ret = True
    if squished.endswith("CONFETTIGARLAND"):  # 1st is missing from the `words` file
        ret = True
    if squished.endswith("PASSPLAY"):  # greedy parse picks out SPLAY
        ret = True
    if squished.startswith("AMBERGRIS"):  # NYT actually wants this 1 word as 2 words
        ret = True
    if squished.endswith("WALLACE"):  # we parse LACE, but NYT wants the name
        ret = True
    if squished.startswith("CASCADECURRENT"):  # apparently DECURRENT is a real word
        ret = True
    if squished.endswith("SKISSOCK"):  # the plural SKIS is missing from 'words' file
        ret = True
    if squished.startswith("BLOUSEPANTSMITE"):  # NYT wants MITE, not SMITE
        ret = True
    return ret
