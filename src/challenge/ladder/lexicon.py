from pathlib import Path

from requests_cache import CachedSession


def get_lexicon() -> set[str]:
    forbidden_chars = set("-'23")  # e.g. "modula-3"
    tmp = Path("/tmp")
    session = CachedSession(
        tmp / "word_list_cache",
        backend="filesystem",
    )
    repo = "https://raw.githubusercontent.com/PeterTheobald/GhostSolver"
    url = f"{repo}/a6b70b6/ubuntu-wordlist.txt"
    resp = session.get(url)
    resp.raise_for_status()
    words = resp.text.lower().rstrip().split("\n")
    # We discard twenty words that contain non-alphabetic characters.
    return {word for word in words if len(forbidden_chars & set(word)) == 0}
