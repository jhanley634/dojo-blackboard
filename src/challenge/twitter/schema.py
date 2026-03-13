from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import (
    Column,
    CreatePoolError,
    Engine,
    ForeignKey,
    Index,
    Integer,
    Text,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


class User(Base):  # type: ignore
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    recent_post = Column(Integer, nullable=False)

    __table_args__ = (Index("idx_user_recent_post_id", "recent_post DESC", "id"),)


class Tweet(Base):  # type: ignore
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    msg = Column(Text)


class Follower(Base):  # type: ignore
    __tablename__ = "follower"

    follower_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    followee_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    __table_args__ = (Index("idx_follower_follower_followee", "follower_id", "followee_id"),)


def create_engine_with_pool() -> Engine:
    """Create engine with proper pool configuration and timeout settings."""
    DB_FILE = Path("/tmp/twitter.db")

    return create_engine(
        f"sqlite:///{DB_FILE}",
        echo=False,
        # Connection pool configuration
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        connect_args={
            "timeout": 30,  # Query timeout
        },
    )


def get_engine() -> Generator[Engine]:
    """Get singleton engine instance with proper context management."""
    _engine: Engine | None = None

    if not isinstance(_engine, Engine):
        global _engine
        _engine = create_engine_with_pool()

    yield _engine

    # Cleanup happens automatically when generator is closed


@contextmanager
def get_session(engine: Engine) -> Generator[Session]:
    """Get a session with proper cleanup and error handling."""
    SessionClass = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    try:
        sess = SessionClass()
        yield sess

        # Auto-commit on successful completion
        if sess.is_autocommit:
            pass  # Already committed in original code
        else:
            sess.commit()

    except Exception:
        sess.rollback()
        raise

    finally:
        sess.close()


# Singleton pattern alternative (if not using generator):
_engine_instance: Engine | None = None


def get_singleton_engine() -> Engine:
    """Get or create singleton engine instance."""
    global _engine_instance

    if _engine_instance is None:
        try:
            with get_engine() as sess:
                return sess.bind  # Get the actual engine from sessionmaker
        except CreatePoolError:
            # Database doesn't exist yet, initialize it
            _engine_instance = create_engine_with_pool()

    return _engine_instance


if __name__ == "__main__":
    with get_session(get_singleton_engine()) as sess:
        print(sess)
