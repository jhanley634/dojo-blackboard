from collections.abc import Generator
from functools import cache
from string import ascii_lowercase

from wordfreq import get_frequency_dict

from challenge.ladder.lexicon import get_lexicon

proposed_cold_to_warm_trace_for__bidi_bfs_ladder = """
## Step-by-Step Trace for "cold" → "warm"

| Step | Queue Fwd | Queue Rev | Visited (Partial) | Meet Found? |
|------|-----------|-----------|-------------------|-------------|
| 0 | `[cold]` | `[warm]` | `{cold: cold}`, `{"": ""}` | No |
| 1 | Process `cold` → expand to `wold`, `fold`, `hold`, `jold`, `kold`, `mold`, `nold`,
`pold`, `qold`, `rold`, `sold`, `told`, `vold`, `wold`, `xold`, `yold` (if valid) | `[warm]`
| `{wold: cold, ...}` | No |
| 2 | Process each forward neighbor → add their neighbors to fwd_q | - | Growing visited_fwd
| No |
| ... | Continue expanding bidirectionally | - | Both sides converge | Yes! |

## Key Variables & Their Expected Values at Meeting Point

```python
# At meeting point 'wold' (or another intermediate word):
visited_fwd = {
    'cold': 'cold',           # start maps to itself
    'wold': 'cold',
    # ... more words in the forward chain
}

visited_rev = {
    'warm': 'warm',          # target maps to itself (or parent)
    'ward': 'warm',
    # ... more words in reverse chain
    'wold': 'wald',          # meeting point!
    # ...
}
```

## Actual Path Components

1. **Forward path from cold to meet:**
   ```python
   ['cold', 'wold']  # or potentially longer depending on lexicon
   ```

2. **Reverse path from warm to meet:**
   ```python
   ['warm', 'ward', 'wald', 'wold']
   ```

3. **Combined path (meeting at 'wold'):**
   ```python
   ['cold', 'wold', 'wald', 'ward', 'warm']  # Length = 5
   ```
"""


def _order_by(word_freq: tuple[str, float]) -> tuple[float, str]:
    word, freq = word_freq
    return 1.0 - freq, word


def bidi_bfs_ladder(
    start: str,
    target: str,
    ranked_words: list[str],
) -> tuple[int, list[str]]:
    """Bidirectional BFS for word ladder."""

    # Use global lexicon if needed, otherwise filter by length
    lexicon = {word for word in ranked_words if len(word) == len(start)}

    assert start in lexicon
    assert target in lexicon
    assert len(start) == len(target)

    # Initialize visited dictionaries and queues
    visited_fwd: dict[str, str] = {start: ""}  # word -> parent
    visited_rev: dict[str, str] = {target: ""}  # word -> parent

    fwd_q: list[str] = [start]
    rev_q: list[str] = [target]

    while fwd_q and rev_q:
        # Expand the smaller queue (swap if needed)
        if len(fwd_q) > len(rev_q):
            fwd_q, rev_q = rev_q, fwd_q
            visited_fwd, visited_rev = visited_rev, visited_fwd

        # Process all nodes in current queue level
        next_q: list[str] = []

        for word in fwd_q:
            # Get neighbors of this word
            for i, nbr_ch in enumerate(ascii_lowercase):
                if i >= len(word):  # Ensure we don't go out of bounds
                    continue
                if nbr_ch == word[i]:
                    continue
                candidate = f"{word[:i]}{nbr_ch}{word[i+1:]}"
                if candidate in lexicon:
                    # Check if neighbor connects to other side (meeting point)
                    if candidate in visited_rev:
                        # Found meeting point - reconstruct path
                        return _reconstruct_path(visited_fwd, visited_rev, word, candidate)

                    # Add to queue if not already visited on this side
                    if candidate not in visited_fwd:
                        visited_fwd[candidate] = word
                        next_q.append(candidate)

        fwd_q = next_q

    return 0, []


def _reconstruct_path(
    visited_fwd: dict[str, str], visited_rev: dict[str, str], meeting_word: str, meet: str
) -> tuple[int, list[str]]:
    """Reconstruct the full path from start to target through the meeting point."""

    # Reconstruct forward path from start to meet
    forward_path: list[str] = []
    word = meeting_word
    while word != "":
        forward_path.append(word)
        word = visited_fwd[word]
    forward_path.reverse()  # start -> meet

    # Reconstruct reverse path from target to meet (reversed order)
    reverse_path: list[str] = []
    word = meet
    while word != "":
        reverse_path.append(word)
        word = visited_rev[word]

    # Combine paths (avoid duplicate at meeting point)
    full_path = forward_path + reverse_path[1:]  # skip the meeting point in reverse path

    cnt = len(forward_path) - 1 + len(reverse_path) - 1
    return cnt, full_path


def get_ranked_words_of_length(n: int, ranked_words: list[str]) -> list[str]:
    """Filter ranked words by length."""
    return [word for word in ranked_words if len(word) == n]


def neighbors(word: str, lexicon: set[str]) -> Generator[str]:
    """Generate neighbor words from lexicon."""
    for i, wrd_ch in enumerate(word):
        prefix = word[:i]
        suffix = word[i + 1 :]

        for nbr_ch in ascii_lowercase.replace(wrd_ch, ""):
            candidate = f"{prefix}{nbr_ch}{suffix}"
            if candidate in lexicon:
                yield candidate


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
