import unittest

from connections.long_word import find_longest_match, find_words


class LongWordTest(unittest.TestCase):

    def test_longest_match(self) -> None:
        pfx, word = find_longest_match("CUPSCAR")
        self.assertEqual("SCAR", word)
        self.assertEqual("CUP", pfx)

    def test_find_words(self) -> None:
        self.assertEqual(["CUP", "SCAR"], find_words("CUPSCAR"))
