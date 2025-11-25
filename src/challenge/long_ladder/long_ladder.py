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


def bidi_bfs_ladder(
    start: str,
    target: str,
    ranked_words: list[str],
) -> list[str]:
    lexicon = set(get_ranked_words_of_length(len(start), ranked_words))
    print(f"{len(lexicon)=}")
    assert start in lexicon
    assert target in lexicon
    assert len(start) == len(target)
    parent_map = {start: ""}
    fwd = {start}
    rev = {target}
    path = [start]
    lexicon.remove(start)
    lexicon.remove(target)
    while fwd:
        if len(fwd) > len(rev):
            fwd, rev = rev, fwd
        nxt = set()

        for word in fwd:
            for nbr in neighbors(word, lexicon):
                parent_map[nbr] = word
                nxt.add(nbr)
                # print(len(fwd), word, nbr)
                # lexicon.remove(nbr)
                if nbr in rev:
                    print(f"{fwd=}")
                    print(f"{len(rev)=}")
                    print(f"{len(parent_map)=}")
                    print(f"{len(lexicon)=}")
                    return construct_path(parent_map, target)

        fwd = nxt

    print(f"{fwd=}")
    print(f"{len(rev)=}")
    print(f"{len(parent_map)=}")
    print(f"{len(lexicon)=}")
    return path


def construct_path(
    parent_map: dict[str, str],
    target: str,
) -> list[str]:
    path: list[str] = []
    word: str | None = target

    while word:
        path.append(f"{word}")
        word = parent_map.get(word)

    return path[::-1]
