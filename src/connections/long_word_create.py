#! /usr/bin/env python

"""
Inits a sqlite database of English words.

We do alphabetic search on *reversed* letters of a word,
since word1 S word2 will tend to pluralize word1.
For example if the original word2 was SCAR,
greedily go for the 4-letter match rather than just CAR.
"""

from pathlib import Path

from sqlalchemy import Column, Engine, Integer, String, Table, __version__, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

TEMP = Path("/tmp")


def get_engine(db_file: Path = Path(TEMP / "words.db")) -> Engine:
    return create_engine(f"sqlite:///{db_file}")


Base = declarative_base()
assert isinstance(Base, DeclarativeMeta)


class Word(Base):  # type: ignore
    __tablename__ = "word"

    rev_word = Column(String, primary_key=True)
    size = Column(Integer)  # word length -- we avoid len() and length() keyword conflict
    word = Column(String)


def etl(in_file: Path = Path("/usr/share/dict/words")) -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)
    seen = set()
    with Session(engine) as sess, open(in_file) as fin:
        # Clear out all rows before we start inserting, to avoid dup PK.
        tbl = Table("word", Base.metadata)
        sess.execute(tbl.delete())

        for line in fin:
            word = line.upper().rstrip()
            if word in seen or len(word) < 3:
                continue
            seen.add(word)
            row = Word(rev_word=word[::-1], size=len(word), word=word)
            sess.add(row)
        sess.commit()


if __name__ == "__main__":
    assert __version__ >= "2.0.41"
    etl()
