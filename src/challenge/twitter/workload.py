from collections.abc import Callable
from dataclasses import dataclass
from itertools import product

import numpy as np
from tqdm import tqdm

from challenge.twitter.schema import get_session

UserId = int
TweetId = int


@dataclass
class Implementation:
    init: Callable[[], None]
    post_tweet: Callable[[UserId, str], TweetId]
    follow: Callable[[UserId, UserId], None]
    unfollow: Callable[[UserId, UserId], None]
    get_news_feed: Callable[[UserId], list[TweetId]]


n_users = 50
rng = np.random.RandomState(seed=42)


def _create_posts(impl: Implementation, n_user_posts: int = 20) -> None:
    """Creates a thousand posts, and the associated 'following' users."""
    impl.init()
    with get_session() as sess:
        for u in range(n_users):
            for p in range(n_user_posts):
                impl.post_tweet(u, f"post {p} from user # {u}")

        n_follows = 20
        user_ids = list(map(int, rng.randint(0, n_users, n_users * n_follows)))
        for u, _ in product(range(n_users), range(n_follows)):
            impl.follow(u, user_ids.pop())

        sess.commit()


def workload(impl: Implementation) -> None:
    _create_posts(impl)
    # A thousand posts down; nine thousand to go...
    user_ids = rng.randint(0, n_users, size=(9_000, 2))  # Some are duplicate, which is fine.
    for p, (u, f) in enumerate(tqdm(user_ids, leave=False, mininterval=0.2)):
        u, f = map(int, (u, f))
        impl.post_tweet(u, f"post {p + 1001}")
        fol_unfol = (impl.follow, impl.unfollow)[p % 2]
        fol_unfol(u, f)
        feed = impl.get_news_feed(u)
        assert len(feed) in range(1, 11)
