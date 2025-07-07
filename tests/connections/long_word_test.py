import unittest

from connections.long_word import find_longest_match


class LongWordTest(unittest.TestCase):

    def test_longest_match(self) -> None:
        find_longest_match("")
