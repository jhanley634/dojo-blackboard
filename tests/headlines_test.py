import unittest

from bboard.newsfeed.headlines import store_current_articles


class HeadlinesTest(unittest.TestCase):

    def test_get_headlines(self) -> None:
        self.assertGreaterEqual(store_current_articles(), 0)
