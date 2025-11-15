import unittest

from challenge.twitter.twitter_pete import (
    Implementation,
    follow,
    init,
    post_tweet,
    test_timeline_basic,
    unfollow,
)


class TwitterPeteTest(unittest.TestCase):
    def test_petes_code(self) -> None:
        test_timeline_basic(Implementation(init, post_tweet, follow, unfollow))
