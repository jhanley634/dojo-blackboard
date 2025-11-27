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
        expected1 = (
            "atlases anlases anlaces unlaces UNLADES unladed unfaded unfamed untamed untimed"
            " unlimed unlined unlines undines ondines ondings endings enrings earings eatings"
            " ratings ratines ravines ravined ravened havened havered tavered tabered tabored"
            " taboret tabaret cabaret".lower()
        )
        assert expected1
        # expected = "cold warm"
        expected = "cold bold bolo"
        start = "cold"
        path = bidi_bfs_ladder(start, "bolo", get_ranked_words())
        self.assertEqual(expected.split(), path)
        self.assertEqual(3, len(path))
