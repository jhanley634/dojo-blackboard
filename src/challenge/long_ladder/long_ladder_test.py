import unittest

import wordfreq

from challenge.long_ladder.long_ladder import (
    bidi_bfs_ladder,
    get_ranked_words,
    get_ranked_words_of_length,
    neighbors,
)


class LongLadderTest(unittest.TestCase):
    def test_get_ranked_words(self) -> None:
        self.assertEqual(42, len(wordfreq.available_languages()))

        self.assertEqual(101_974, len(get_ranked_words()))

    def test_neighbors(self) -> None:
        word = "warm"
        lexicon = set(get_ranked_words_of_length(len(word), get_ranked_words()))
        expected = "barm farm harm marm warb ward ware wark warn warp wars wart wary wasm worm"
        self.assertEqual(expected.split(), sorted(neighbors(word, lexicon)))
        self.assertEqual(4_844, len(lexicon))

        self.assertIn("bold", neighbors("cold", lexicon))
        self.assertIn("bolo", neighbors("bold", lexicon))

        self.assertIn("cold", neighbors("bold", lexicon))
        self.assertIn("bold", neighbors("bolo", lexicon))

    def test_find_path_4(self) -> None:
        expected = "cold wold word ward warm"
        cnt, path = bidi_bfs_ladder("cold", "warm", get_ranked_words())
        self.assertEqual(expected.split(), path)
        self.assertEqual(3, cnt)

    def disabled_test_find_path_6b(self) -> None:
        expected = (
            "charge change changs clangs clanks cranks cranes crates coates contes"
            " montes mantes mattes maties matins mating dating doting doming homing"
            " hominy homily homely comely comedy comedo"
        )
        cnt, path = bidi_bfs_ladder("charge", "comedo", get_ranked_words())
        print(" ".join(path))
        self.assertEqual(expected, " ".join(path))
        self.assertEqual(26, len(path))
        self.assertEqual(5_622, cnt)
