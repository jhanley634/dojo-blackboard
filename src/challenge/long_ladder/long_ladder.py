from collections.abc import Generator
from functools import cache
from string import ascii_lowercase

from wordfreq import get_frequency_dict

from challenge.ladder.lexicon import get_lexicon

proposed_cold_to_warm_trace_for__bidi_bfs_ladder = """
## Step-by-Step Trace for "cold" → "warm", first seven entries

| fwd_q                              | rev_q                              |
|------------------------------------+------------------------------------|
| cold                               | warm                               |
| warm                               | bold fold gold hold mold sold told |
| barm farm harm marm worm wasm warb | bold fold gold hold mold sold told |
| bold fold gold hold mold sold told | berm balm barb bard bare barf bark |
"""


def _order_by(word_freq: tuple[str, float]) -> tuple[float, str]:
    word, freq = word_freq
    return 1.0 - freq, word


def neighbors(word: str, lexicon: set[str]) -> Generator[str]:
    """Generate neighbor words from lexicon."""
    for i in range(len(word)):
        prefix = word[:i]
        suffix = word[i + 1 :]

        for nbr_ch in ascii_lowercase:
            if nbr_ch == word[i]:
                continue
            candidate = f"{prefix}{nbr_ch}{suffix}"
            if candidate in lexicon:
                yield candidate


def bidi_bfs_ladder(
    start: str,
    target: str,
    ranked_words: list[str],
) -> tuple[int, list[str]]:
    """Bidirectional BFS for word ladder."""

    lexicon = {word for word in ranked_words if len(word) == len(start)}

    assert start in lexicon
    assert target in lexicon
    assert len(start) == len(target)

    visited_fwd: dict[str, str] = {start: ""}
    visited_rev: dict[str, str] = {target: ""}

    fwd_q: list[str] = [start]
    rev_q: list[str] = [target]

    while fwd_q and rev_q:
        if len(fwd_q) > len(rev_q):
            fwd_q, rev_q = rev_q, fwd_q
            visited_fwd, visited_rev = visited_rev, visited_fwd

        next_q: list[str] = []

        for word in fwd_q:
            for nbr in neighbors(word, lexicon):
                if nbr in visited_fwd:
                    continue

                visited_fwd[nbr] = word
                next_q.append(nbr)

                if nbr in visited_rev:
                    return _reconstruct_path(visited_fwd, visited_rev, word, nbr)

        fwd_q = next_q

    return 0, []


def _reconstruct_path(
    visited_fwd: dict[str, str], visited_rev: dict[str, str], meeting_word: str, meet: str
) -> tuple[int, list[str]]:
    """Reconstruct the full path from start to target through the meeting point."""

    # Reconstruct forward path from start to meeting_word
    forward_path = []
    word = meeting_word
    while word != "":
        forward_path.append(word)
        word = visited_fwd[word]
    forward_path.reverse()

    # Reconstruct reverse path from target to meet
    reverse_path = []
    word = meet
    while word != "":
        reverse_path.append(word)
        word = visited_rev[word]

    full_path = forward_path + reverse_path
    all_words = get_ranked_words_of_length(len(meet), get_ranked_words())
    tot_rank = sum(all_words.index(word) for word in full_path)
    return tot_rank, full_path


def get_ranked_words_of_length(n: int, ranked_words: list[str]) -> list[str]:
    """Filter ranked words by length."""
    return [word for word in ranked_words if len(word) == n]


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
