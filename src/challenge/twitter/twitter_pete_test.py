import unittest

from challenge.twitter.twitter_pete import (
    Implementation,
    follow,
    init,
    test_timeline_basic,
    tweet,
    unfollow,
)


class TwitterPeteTest(unittest.TestCase):
    def test_petes_code(self) -> None:
        test_timeline_basic(Implementation(init, tweet, follow, unfollow))
