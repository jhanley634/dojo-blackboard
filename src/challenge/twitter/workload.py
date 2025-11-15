from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from challenge.twitter.schema import User, get_session

UserId = int
TweetId = int


@dataclass
class Implementation:
    init: Callable[[], None]
    post_tweet: Callable[[UserId, str], TweetId]
    follow: Callable[[UserId, UserId], None]
    unfollow: Callable[[UserId, UserId], None]
    get_news_feed: Callable[[UserId], list[TweetId]]


def _create_posts(impl: Implementation, n_users: int = 50, n_user_posts: int = 20) -> None:
    """Creates a thousand posts, and the associated following users."""
    impl.init()
    with get_session() as sess:
        for u in range(n_users):
            sess.add(User(id=u))
            for p in range(n_user_posts):
                impl.post_tweet(u, f"post {p} from user # {u}")

        n_follows = 20
        rng = np.random.RandomState(seed=42)
        user_ids = list(map(int, rng.randint(0, n_users, n_users * n_follows)))
        for u in range(n_users):
            for _ in range(n_follows):
                impl.follow(u, user_ids.pop())

        sess.commit()


def workload(impl: Implementation) -> None:
    _create_posts(impl)
