import unittest

from challenge.ladder.word_ladder import find_word_path


class WordLadderTest(unittest.TestCase):
    def test_find_path(self) -> None:
        lexicon = {"hit", "hot", "dot", "dog", "lot", "log", "cog"}
        self.assertEqual(
            ["hit", "hot", "dot", "dog", "cog"],
            find_word_path("hit", "cog", lexicon),
        )
