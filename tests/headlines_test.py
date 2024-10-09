import unittest
from warnings import catch_warnings, simplefilter

from bboard.newsfeed.headlines import _href, store_current_articles


class HeadlinesTest(unittest.TestCase):

    def test_href(self) -> None:
        self.assertEqual(
            '<a href="https://example.com">an example</a>',
            _href("https://example.com", "an example"),
        )

    def test_get_headlines(self) -> None:
        with catch_warnings():
            simplefilter("ignore", category=DeprecationWarning)
            with catch_warnings():
                simplefilter("ignore", category=FutureWarning)

                self.assertGreaterEqual(store_current_articles(), 0)
