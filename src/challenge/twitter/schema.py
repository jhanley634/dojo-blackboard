from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Column, Engine, ForeignKey, Integer, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


class User(Base):  # type: ignore
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)


class Tweet(Base):  # type: ignore
    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    msg = Column(Text)


class Follower(Base):  # type: ignore
    __tablename__ = "follower"
    follower_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    followee_id = Column(Integer, ForeignKey("user.id"), primary_key=True)


def workload() -> None:
    q = 1
    assert q


DB_FILE = Path("/tmp/twitter.db")

_engine: list[Engine] = []


def get_engine() -> Engine:
    if not _engine:
        _engine.append(
            create_engine(f"sqlite:///{DB_FILE}", echo_pool=False),
        )
    return _engine[0]


@contextmanager
def get_session() -> Generator[Session]:  # pyright: ignore
    with sessionmaker(bind=get_engine())() as sess:
        yield sess
        sess.commit()


if __name__ == "__main__":
    with get_session() as sess:
        print(sess)

    Base.metadata.create_all(get_engine())
