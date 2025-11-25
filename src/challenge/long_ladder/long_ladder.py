from collections.abc import Generator
from functools import cache
from string import ascii_lowercase

from wordfreq import get_frequency_dict

from challenge.ladder.lexicon import get_lexicon


def _order_by(word_freq: tuple[str, float]) -> tuple[float, str]:
    word, freq = word_freq
    return 1.0 - freq, word


@cache
def get_ranked_words() -> list[str]:
    """Returns a lexicon list, with the most common words appearing first.

    Word frequencies are quantized to centiBels within the wordfreq package.
    Toward the end of the list, words with identical frequency values
    appear in alphabetic order.
    """
    assert 267_752 == len(get_lexicon())
    word_to_freq = dict(sorted(get_frequency_dict("en").items(), key=_order_by))
    words = set(word_to_freq.keys()).intersection(get_lexicon())
    assert 101_974 == len(words)

    return [word for word in word_to_freq if word in words]


def get_ranked_words_of_length(n: int, ranked_words: list[str]) -> list[str]:
    return [word for word in ranked_words if len(word) == n]


def neighbors(word: str, lexicon: set[str]) -> Generator[str]:
    for i, wrd_ch in enumerate(word):
        prefix = word[:i]
        suffix = word[i + 1 :]
        assert word == f"{prefix}{wrd_ch}{suffix}"

        for nbr_ch in ascii_lowercase.replace(wrd_ch, ""):
            candidate = f"{prefix}{nbr_ch}{suffix}"
            if candidate in lexicon:
                yield candidate


def bidi_bfs_ladder(start: str, target: str, ranked_words: list[str]) -> list[str]:
    lexicon = get_ranked_words_of_length(len(start), ranked_words)
    assert start in lexicon
    assert target in lexicon
    assert len(start) == len(target)
    fwd = {start}
    rev = {target}
    lexicon.remove(start)
    lexicon.remove(target)
    path: list[str] = []
    while False:
        if len(fwd) > len(rev):
            fwd, rev = rev, fwd
        for word in fwd:
            for nbr in neighbors(word, lexicon):
                fwd.add(nbr)

    return path
