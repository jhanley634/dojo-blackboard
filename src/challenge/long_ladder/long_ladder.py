from collections.abc import Generator
from dataclasses import dataclass
from functools import cache
from pprint import pp
from queue import Queue
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


# start --> target goes from left to right
@dataclass
class Node:
    val: str
    parent: str | None
    target_side: bool


class WordQueue(Queue[str]):
    def __init__(self, maxsize: int = 0, *, is_fwd: bool = False) -> None:
        super().__init__(maxsize)
        self.is_fwd = is_fwd


def bidi_bfs_ladder(
    start: str,
    target: str,
    ranked_words: list[str],
) -> tuple[int, list[str]]:
    lexicon = set(get_ranked_words_of_length(len(start), ranked_words))
    assert start in lexicon
    assert target in lexicon
    assert len(start) == len(target)

    cnt = 0
    visited = {start: start}
    fwd_q: WordQueue = WordQueue()
    fwd_q.put(start)
    a = fwd_q
    while a.not_empty:
        word = a.get()
        for nbr in neighbors(word, lexicon):
            if nbr == target:
                visited[nbr] = word
                print(f"{cnt=}")
                return cnt, construct_path(visited, start, target)
            if nbr not in visited:
                visited[nbr] = word
                a.put(nbr)
                cnt += 1

    return cnt, []


def construct_path(
    visited: dict[str, str],
    start: str,
    target: str,
) -> list[str]:
    # `visited` has a chain of words from `target` back to `start`
    assert start
    assert target
    pp(visited)

    path: list[str] = []
    word = target
    while word != start:
        path.append(word)
        word = visited[word]
    path.append(word)

    path.reverse()
    return path
