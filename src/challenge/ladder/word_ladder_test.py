import unittest

from challenge.ladder.anagram import find_anagrams, lexicon
from challenge.ladder.lexicon import get_lexicon
from challenge.ladder.word_ladder import find_word_path


class WordLadderTest(unittest.TestCase):

    def test_get_lexicon(self) -> None:
        self.assertEqual(178_691, len(get_lexicon()))

    def test_anagram(self) -> None:
        self.assertEqual(
            ["caller", "cellar", "recall"],
            find_anagrams("recall"),
        )
        self.assertEqual([], find_anagrams("does not exist"))

    def test_find_path_3(self) -> None:
        small_lexicon = {"hit", "hot", "dot", "dog", "lot", "log", "cog"}
        self.assertEqual(
            ["hit", "hot", "dot", "dog", "cog"],
            find_word_path("hit", "cog", small_lexicon),
        )
        self.assertEqual(
            ["hit", "hot", "hog", "cog"],
            find_word_path("hit", "cog", lexicon),
        )

    def test_find_path_4(self) -> None:
        self.assertEqual(
            [
                "cold",
                "wold",
                "word",
                "worm",
                "warm",
            ],
            find_word_path("cold", "warm", lexicon),
        )

    def test_find_path_5a(self) -> None:
        self.assertEqual(
            [
                "horse",
                "corse",
                "carse",
                "carle",
                "carls",
                "cares",
                "rares",
                "races",
            ],
            find_word_path("horse", "races", lexicon),
        )

    def test_find_path_5b(self) -> None:
        self.assertEqual(
            [
                "small",
                "shall",
                "shill",
                "shiel",
                "shied",
                "shred",
                "sired",
                "siree",
                "saree",
                "sarge",
                "large",
            ],
            find_word_path("small", "large", lexicon),
        )

    def test_find_path_6(self) -> None:
        self.assertEqual(
            [
                "listen",
                "lister",
                "laster",
                "baster",
                "barter",
                "barber",
            ],
            find_word_path("listen", "barber", lexicon),
        )
