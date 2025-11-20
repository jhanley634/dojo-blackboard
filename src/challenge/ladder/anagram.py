from collections import defaultdict

from challenge.ladder.lexicon import get_lexicon


def _canonical_form(word: str) -> str:
    return "".join(sorted(word))


def _get_anagrams_dict(lexicon: set[str]) -> dict[str, set[str]]:
    ret: dict[str, set[str]] = defaultdict(set)
    for word in lexicon:
        ret[_canonical_form(word)].add(word)
    return ret


lexicon = get_lexicon()
anagrams = _get_anagrams_dict(lexicon)


def find_anagrams(word: str) -> list[str]:
    return sorted(anagrams[_canonical_form(word)])
