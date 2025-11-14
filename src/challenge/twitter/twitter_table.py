from typing import cast

from challenge.twitter.schema import Base, Follower, Tweet, User, get_engine, get_session
from challenge.twitter.twitter_pete import Implementation, TweetId, UserId


def init() -> None:
    """Ensures we have three empty tables."""

    Base.metadata.create_all(get_engine())

    with get_session() as sess:
        sess.query(Tweet).delete()
        sess.query(User).delete()
        sess.query(Follower).delete()
        sess.commit()


def tweet(my_id: UserId, content: str) -> TweetId:
    with get_session() as sess:
        tw = Tweet(user_id=my_id, msg=content)
        sess.add(tw)
        sess.commit()
        return cast("int", tw.id)


def follow(my_id: int, to_follow_id: int) -> None: ...


def unfollow(my_id: int, to_unfollow_id: int) -> None: ...


_impl = Implementation(init, tweet, follow, unfollow)
