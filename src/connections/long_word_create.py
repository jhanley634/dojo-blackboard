#! /usr/bin/env python

"""
Inits a sqlite database of English words.

We index on reversed word spellings in order to support
the queries issued by find_longest_match().
"""

from pathlib import Path

from sqlalchemy import Column, Engine, String, __version__, create_engine, inspect
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

TEMP = Path("/tmp")
WORDS_DB = TEMP / "words.db"


class DbMgr:
    _engine: Engine | None = None  # singleton

    @classmethod
    def get_engine(cls, db_file: Path = WORDS_DB) -> Engine:
        if cls._engine is None:
            cls._engine = create_engine(f"sqlite:///{db_file}")
        return cls._engine


def table_exists(table_name: str) -> bool:
    inspector = inspect(DbMgr.get_engine())
    return inspector.has_table(table_name)


Base = declarative_base()
assert isinstance(Base, DeclarativeMeta)


class Word(Base):  # type: ignore
    __tablename__ = "word"

    rev_word = Column(String, primary_key=True)
    word = Column(String)


ENGLISH_WORDS = Path("/usr/share/dict/words")


def etl(in_file: Path = ENGLISH_WORDS) -> None:
    engine = DbMgr.get_engine()
    Base.metadata.create_all(engine)
    assert table_exists("word")
    seen = set()
    with Session(engine) as sess, open(in_file) as fin:
        # Clear out all rows before we start inserting, to avoid dup PK.
        sess.query(Word).delete()

        for line in fin:
            word = line.upper().rstrip()
            if word in seen or len(word) < 3:
                continue
            seen.add(word)
            row = Word(rev_word=word[::-1], word=word)
            sess.add(row)
        sess.commit()


if __name__ == "__main__":
    assert __version__ >= "2.0.41"
    etl()
