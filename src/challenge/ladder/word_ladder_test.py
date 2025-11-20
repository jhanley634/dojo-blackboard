import re
import unittest

from challenge.ladder.anagram import find_anagrams, lexicon
from challenge.ladder.lexicon import get_lexicon
from challenge.ladder.scrape import scrape_long_ladders
from challenge.ladder.word_ladder import find_word_path


class WordLadderTest(unittest.TestCase):

    def test_get_lexicon(self, *, verbose: bool = False) -> None:

        self.assertEqual(267_752, len(get_lexicon()))

        cnt = dict.fromkeys(range(2, 16), 0)
        alpha_re = re.compile("^[a-z]+$")
        for word in get_lexicon():
            cnt[len(word)] += 1
            assert alpha_re.search(word), word

        if verbose:
            print()
            for k, v in cnt.items():
                print(f" {v:6,} words of length {k:2}")

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
            ["cold", "wold", "wald", "ward", "warm"],
            find_word_path("cold", "warm", lexicon),
        )

    def test_find_path_5a(self) -> None:
        self.assertEqual(
            ["horse", "corse", "carse", "carle", "carls", "cares", "rares", "races"],
            find_word_path("horse", "races", lexicon),
        )

    def test_find_path_5b(self) -> None:
        self.assertEqual(
            ["small", "scall", "scale", "scare", "seare", "serre", "serge", "sarge", "large"],
            find_word_path("small", "large", lexicon),
        )

    def test_find_path_6a(self) -> None:
        self.assertEqual(
            ["listen", "lister", "laster", "baster", "barter", "barber"],
            find_word_path("listen", "barber", lexicon),
        )

    def test_find_path_6b(self) -> None:
        expected = (
            "charge change changs chanks cranks cranes crates coates contes conies"
            " conins coning coming homing hominy homily homely comely comedy comedo"
        )
        path = find_word_path("charge", "comedo", lexicon)
        self.assertEqual(20, len(path))
        self.assertEqual(expected.split(), path)

    def test_find_path_7(self) -> None:
        expected = (
            "atlases anlases anlaces unlaces UNLADES unladed unfaded unfamed untamed untimed"
            " unlimed unlined unlines undines ondines ondings endings enrings earings eatings"
            " ratings ratines ravines ravined ravened havened havered tavered tabered tabored"
            " taboret tabaret cabaret".lower()
        )
        path = find_word_path("atlases", "cabaret", lexicon)
        self.assertEqual(33, len(path))
        self.assertEqual(expected.split(), path)

    def test_scrape_long_ladders(self, *, verbose: bool = False) -> None:
        for ladder in scrape_long_ladders():
            start, target = ladder[0], ladder[-1]
            path = find_word_path(start, target, lexicon)
            if verbose:
                print("\n", len(ladder), len(path), start, target)
            self.assertLessEqual(len(path), len(ladder))
            if len(ladder) == len(path):
                self.assertEqual(ladder, path)
