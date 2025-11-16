from collections.abc import Callable
from dataclasses import dataclass
from itertools import product

from numpy.random import RandomState
from tqdm import tqdm

from challenge.twitter.schema import get_session

UserId = int
TweetId = int

# These come from the original problem specification.
valid_user_id_range = range(500)
valid_tweet_id_range = range(1, 10_001)


@dataclass
class Implementation:
    init: Callable[[], None]
    post_tweet: Callable[[UserId, str], TweetId]
    follow: Callable[[UserId, UserId], None]
    unfollow: Callable[[UserId, UserId], None]
    get_news_feed: Callable[[UserId], list[TweetId]]


n_users = 50


def _create_posts(impl: Implementation, rng: RandomState, n_user_posts: int = 20) -> None:
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


def workload(impl: Implementation) -> tuple[UserId, UserId, list[TweetId]]:
    rng = RandomState(seed=42)
    _create_posts(impl, rng)
    # A thousand posts down; nine thousand to go...
    u, f = 0, 0
    feed = []
    user_ids = rng.randint(0, n_users, size=(9_000, 2))  # Some are duplicate, which is fine.
    for p, (u, f) in enumerate(tqdm(user_ids, leave=False, mininterval=0.2)):
        u, f = map(int, (u, f))
        impl.post_tweet(u, f"post {p + 1001}")
        fol_unfol = (impl.follow, impl.unfollow)[p % 2]
        fol_unfol(u, f)
        feed = impl.get_news_feed(u)
        assert len(feed) in range(1, 11)

    return u, f, feed


expected_final_feed = [10000, 9999, 9998, 9995, 9994, 9993, 9992, 9991, 9989, 9987]
