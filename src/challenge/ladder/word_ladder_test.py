import unittest

from challenge.ladder.lexicon import get_lexicon
from challenge.ladder.word_ladder import find_word_path


class WordLadderTest(unittest.TestCase):

    def test_get_lexicon(self) -> None:
        self.assertEqual(45_402, len(get_lexicon()))

    def test_find_path_3(self) -> None:
        small_lexicon = {"hit", "hot", "dot", "dog", "lot", "log", "cog"}
        self.assertEqual(
            ["hit", "hot", "dot", "dog", "cog"],
            find_word_path("hit", "cog", small_lexicon),
        )
        self.assertEqual(
            ["hit", "hot", "cot", "cog"],
            find_word_path("hit", "cog", get_lexicon()),
        )

    def test_find_path_5(self) -> None:
        self.assertEqual(
            [
                "horse",
                "house",
                "louse",
                "loose",
                "noose",
                "noise",
                "poise",
                "posse",
                "passe",
                "paste",
                "pasts",
                "pacts",
                "paces",
                "races",
            ],
            find_word_path("horse", "races", get_lexicon()),
        )
