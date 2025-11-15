from operator import attrgetter
from typing import cast

from sqlalchemy.exc import IntegrityError

from challenge.twitter.schema import Base, Follower, Tweet, User, get_engine, get_session
from challenge.twitter.twitter_pete import TweetId, UserId


def init(n_users: int = 500) -> None:
    """Ensures we have two empty tables."""
    # The original problem spec constrains us to 500 users max.

    Base.metadata.create_all(get_engine())

    with get_session() as sess:
        sess.query(Tweet).delete()
        sess.query(Follower).delete()
        sess.query(User).delete()

        for u in range(n_users):
            sess.add(User(id=u))

        sess.commit()


def post_tweet(my_id: UserId, content: str) -> TweetId:
    with get_session() as sess:
        tw = Tweet(user_id=my_id, msg=content)
        sess.add(tw)
        sess.commit()
        return cast("int", tw.id)


def follow(my_id: UserId, to_follow_id: UserId) -> None:
    with get_session() as sess:
        try:
            sess.add(Follower(follower_id=my_id, followee_id=to_follow_id))
            sess.commit()
        except IntegrityError:  # duplicate UNIQUE key
            # Already followed so there's nothing to do; follow() is idempotent.
            sess.rollback()


def unfollow(my_id: UserId, to_unfollow_id: UserId) -> None:
    with get_session() as sess:
        sess.query(Follower).filter_by(follower_id=my_id, followee_id=to_unfollow_id).delete()
        sess.commit()


def get_news_feed(my_id: UserId, limit: int = 10) -> list[TweetId]:
    follow(my_id, my_id)  # I always follow my own posts.
    with get_session() as sess:
        q = (
            sess.query(Tweet)
            .join(Follower, Follower.followee_id == Tweet.user_id)
            .filter(Follower.follower_id == my_id)
            .order_by(Tweet.id.desc())
            .limit(limit)
        )
        return list(map(attrgetter("id"), q.all()))
