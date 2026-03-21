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

        self.assertIn("word", lexicon)
        self.assertIn("word", neighbors("wold", lexicon))
        self.assertEqual(
            "bold cold fold gold hold mold sold told wald weld wild woad wood word wolf",
            " ".join(neighbors("wold", lexicon)),
        )

    def test_find_path_4(self) -> None:
        expected = "cold wold wald ward warm"
        cnt, path = bidi_bfs_ladder("cold", "warm", get_ranked_words())
        self.assertEqual(expected.split(), path)
        self.assertEqual(5_961, cnt)

    def test_find_path_6b(self) -> None:
        expected = (
            "comedy comely homely homily hominy homing doming"
            " doting dating mating matins maties mattes mantes montes contes coates"
            " crates cranes cranks clanks clangs changs change charge"
        )
        cnt, path = bidi_bfs_ladder("comedy", "charge", get_ranked_words())
        self.assertEqual(expected, " ".join(path))
        self.assertEqual(25, len(path))
        self.assertEqual(126_561, cnt)
