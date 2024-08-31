from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(url="sqlite:////tmp/blackboard.db")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    sess = sessionmaker(bind=engine)()
    try:
        yield sess
    finally:
        sess.commit()
