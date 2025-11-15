from collections.abc import Callable
from dataclasses import dataclass

from tqdm import tqdm

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


def _create_posts(impl: Implementation, n_users: int = 50, n_user_posts: int = 100) -> None:
    """Creates ten thousand posts, and the associated following users."""
    impl.init()
    print()
    with get_session() as sess:
        for u in tqdm(range(n_users), leave=False):
            sess.add(User(id=u))
            for p in range(n_user_posts):
                impl.post_tweet(u, f"post {p} from user # {u}")
        for u in range(n_users):
            for f in range(max(u, 20)):
                impl.follow(u, f)
        sess.commit()


def workload(impl: Implementation) -> None:
    _create_posts(impl)
