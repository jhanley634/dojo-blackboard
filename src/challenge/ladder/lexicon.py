from pathlib import Path

from requests_cache import CachedSession


def get_lexicon() -> set[str]:
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
    return set(words)
