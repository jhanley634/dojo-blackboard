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


def follow(my_id: UserId, to_follow_id: UserId) -> None: ...


def unfollow(my_id: UserId, to_unfollow_id: UserId) -> None: ...


def users_tweets(my_id: UserId, limit: int = 10) -> list[Tweet]:
    with get_session() as sess:
        assert sess
        assert my_id < limit
    return []


_impl = Implementation(init, tweet, follow, unfollow)
