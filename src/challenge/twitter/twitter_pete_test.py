import unittest

from challenge.twitter.twitter_pete import (
    follow,
    get_news_feed,
    init,
    post_tweet,
    tst_timeline_basic,
    unfollow,
)
from challenge.twitter.workload import Implementation, workload

_impl = Implementation(init, post_tweet, follow, unfollow, get_news_feed)


class TwitterPeteTest(unittest.TestCase):
    def test_petes_code(self) -> None:
        tst_timeline_basic(_impl)

    def test_pete_with_workload(self) -> None:
        # This runs in ~ 450 msec.
        workload(_impl)
