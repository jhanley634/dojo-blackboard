from sqlalchemy.orm import Session

from connections.long_word_create import Word, get_engine


def find_longest_match(squished: str) -> tuple[str, str]:
    """Breaks a squished string into two pieces.

    The pieces are a prefix of zero or more squished words,
    plus an English word matching the end.

    We do alphabetic search on *reversed* letters of a word.
    Otherwise word1 S word2 will tend to pluralize word1.
    For example if the original word2 was SCAR,
    greedily go for the 4-letter match rather than just CAR.
    """
    rev_squished = squished[::-1]
    wildcard = rev_squished[:3] + "%"
    match = ""
    with Session(get_engine()) as sess:
        query = sess.query(Word).filter(Word.rev_word.like(wildcard))
        for row in query:
            rev_word = f"{row.rev_word}"
            if rev_squished.startswith(rev_word) and len(rev_word) > len(match):
                match = f"{row.word}"

    pfx = squished[: -len(match)]
    assert f"{pfx}{match}" == squished, (pfx, match, squished)
    return pfx, match


def find_words(squished: str) -> list[str]:
    assert " " not in squished
    ret: list[str] = []
    while squished:
        squished, word = find_longest_match(squished)
        ret.append(word)
    return list(reversed(ret))
