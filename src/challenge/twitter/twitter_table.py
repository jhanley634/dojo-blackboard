from operator import attrgetter
from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.query import Query

from challenge.twitter.schema import Base, Follower, Tweet, User, get_engine, get_session
from challenge.twitter.workload import TweetId, UserId, valid_tweet_id_range, valid_user_id_range


def init(n_users: int = 500) -> None:
    """Ensures we have two empty tables."""
    # The original problem spec constrains us to 500 users max.
    assert n_users - 1 in valid_user_id_range

    Base.metadata.create_all(get_engine())
    # Create a couple of covering indexes.
    sql1 = "CREATE INDEX idx_tweet_user_id_id ON tweet (user_id, id DESC)"
    sql2 = "CREATE INDEX idx_follower_follower_followee ON follower (follower_id, followee_id)"

    with get_session() as sess:
        sess.execute(text("DROP INDEX  IF EXISTS  idx_tweet_user_id_id"))
        sess.execute(text("DROP INDEX  IF EXISTS  idx_follower_follower_followee"))
        sess.execute(text(sql1))
        sess.execute(text(sql2))
        sess.query(Tweet).delete()
        sess.query(Follower).delete()
        sess.query(User).delete()

        for u in range(n_users):
            sess.add(User(id=u))

        sess.commit()


def post_tweet(my_id: UserId, content: str) -> TweetId:
    assert my_id in valid_user_id_range

    with get_session() as sess:
        tw = Tweet(user_id=my_id, msg=content)
        sess.add(tw)
        sess.commit()
        created_id = cast("int", tw.id)
        assert created_id in valid_tweet_id_range
        return created_id


def follow(my_id: UserId, to_follow_id: UserId) -> None:
    assert my_id in valid_user_id_range
    assert to_follow_id in valid_user_id_range

    with get_session() as sess:
        try:
            sess.add(Follower(follower_id=my_id, followee_id=to_follow_id))
            sess.commit()
        except IntegrityError:  # duplicate UNIQUE key
            # Already followed so there's nothing to do; follow() is idempotent.
            sess.rollback()


def unfollow(my_id: UserId, to_unfollow_id: UserId) -> None:
    assert my_id in valid_user_id_range
    assert to_unfollow_id in valid_user_id_range

    with get_session() as sess:
        sess.query(Follower).filter_by(follower_id=my_id, followee_id=to_unfollow_id).delete()
        sess.commit()


def get_news_feed(my_id: UserId, limit: int = 10) -> list[TweetId]:
    assert my_id in valid_user_id_range

    follow(my_id, my_id)  # I always follow my own posts.

    with get_session() as sess:
        q = (
            sess.query(Tweet.id)
            .join(Follower, Follower.followee_id == Tweet.user_id)
            .filter(Follower.follower_id == my_id)
            .order_by(Tweet.id.desc())
            .limit(limit)
        )
        return list(map(attrgetter("id"), q.all()))


def _explain(query: Query[Any]) -> None:
    sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    with get_engine().connect() as conn:
        plan = conn.execute(text(f"EXPLAIN QUERY PLAN {sql}"))
        for row in plan:
            print(row)
