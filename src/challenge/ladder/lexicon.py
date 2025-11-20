import re
from pathlib import Path

from requests_cache import CachedSession


def cached_session() -> CachedSession:
    tmp = Path("/tmp")
    return CachedSession(
        tmp / "word_list_cache",
        backend="filesystem",
    )


def get_lexicon() -> set[str]:
    forbidden_chars = set("-'23")  # e.g. "modula-3"
    discard_preamble_re = re.compile(r"^sowpods.*download/english.txt..", re.DOTALL)
    # repo = "https://raw.githubusercontent.com/PeterTheobald/GhostSolver"
    # url = f"{repo}/a6b70b6/ubuntu-wordlist.txt"  # 45_353 words
    # url = f"{repo}/a6b70b6/TWL06-wordlist.txt"  # 178_691 words
    url = "https://www.freescrabbledictionary.com/sowpods/download/sowpods.txt"
    resp = cached_session().get(url)
    resp.raise_for_status()
    words = resp.text.lower().replace("\r", "").rstrip()
    words = discard_preamble_re.sub("", words)
    # We discard words that contain non-alphabetic characters.
    return {word for word in words.split() if len(forbidden_chars & set(word)) == 0}
