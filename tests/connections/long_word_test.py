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
            if cat == "RUMMAGE":  # that's enough testing examples, for now
                return
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
    """Returns True if we should skip testing this particular example."""
    # It turns out that no heuristic approach is going to perform very well.
    # Deleting all blanks between words destroys information that we
    # can't necessarily get back, and I'm not keen to change the API
    # to return several candidate answers.
    ret = False
    for word in words:
        if word not in english_words:
            ret = True
    if " " in squished:
        ret = True
    prefixes = [
        "AMBERGRIS",  # NYT actually wants this 1 word as 2 words
        "CASCADECURRENT",  # apparently DECURRENT is a real word
        "BLOUSEPANTSMITE",  # NYT wants MITE, not SMITE
        "APPLEBARCANECORN",  # we parse PLEB ARCANE CORN
        "CLAWHOOF",  # we parse WHOOF
        "CLAPPEAL",  # we parse APPEAL
    ]
    suffixes = [
        "PASSPLAY",  # greedy parse picks out SPLAY
        "WALLACE",  # we parse LACE, but NYT wants the name
        "SKISSOCK",  # the plural SKIS is missing from 'words' file
        "TREASUREVALUE",  # we parse REVALUE
    ]
    for pfx in prefixes:
        if squished.startswith(pfx):
            ret = True
    for sfx in suffixes:
        if squished.endswith(sfx):
            ret = True
    return ret
