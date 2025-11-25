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

    def test_find_path_7(self) -> None:
        expected = (
            "atlases anlases anlaces unlaces UNLADES unladed unfaded unfamed untamed untimed"
            " unlimed unlined unlines undines ondines ondings endings enrings earings eatings"
            " ratings ratines ravines ravined ravened havened havered tavered tabered tabored"
            " taboret tabaret cabaret".lower()
        )
        start = "atlases"
        path = bidi_bfs_ladder(start, "cabaret", get_ranked_words())
        self.assertEqual(33, len(path))
        self.assertEqual(expected.split(), path)
