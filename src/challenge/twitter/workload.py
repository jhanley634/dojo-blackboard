from collections.abc import Callable
from dataclasses import dataclass

UserId = int
TweetId = int


@dataclass
class Implementation:
    init: Callable[[], None]
    post_tweet: Callable[[UserId, str], TweetId]
    follow: Callable[[UserId, UserId], None]
    unfollow: Callable[[UserId, UserId], None]
    get_news_feed: Callable[[UserId], list[TweetId]]
