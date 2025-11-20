import unittest

from challenge.ladder.anagram import find_anagrams, lexicon
from challenge.ladder.lexicon import get_lexicon
from challenge.ladder.word_ladder import find_word_path


class WordLadderTest(unittest.TestCase):

    def test_get_lexicon(self) -> None:
        self.assertEqual(45_353, len(get_lexicon()))

    def test_anagram(self) -> None:
        self.assertEqual(
            ["caller", "cellar", "recall"],
            find_anagrams("recall"),
        )

    def test_find_path_3(self) -> None:
        small_lexicon = {"hit", "hot", "dot", "dog", "lot", "log", "cog"}
        self.assertEqual(
            ["hit", "hot", "dot", "dog", "cog"],
            find_word_path("hit", "cog", small_lexicon),
        )
        self.assertEqual(
            ["hit", "hot", "cot", "cog"],
            find_word_path("hit", "cog", lexicon),
        )

    def test_find_path_5(self) -> None:
        self.assertEqual(
            [
                "horse",
                "norse",
                "nurse",
                "purse",
                "parse",
                "parke",
                "parks",
                "packs",
                "paces",
                "races",
            ],
            find_word_path("horse", "races", lexicon),
        )

    def test_find_path_6(self) -> None:
        self.assertEqual(
            [
                "listen",
                "lister",
                "litter",
                "bitter",
                "batter",
                "barter",
                "barber",
            ],
            find_word_path("listen", "barber", lexicon),
        )
