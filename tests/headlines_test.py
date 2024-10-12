import unittest
from warnings import catch_warnings, simplefilter

from bboard.newsfeed.headlines import _href, store_current_articles
from bboard.newsfeed.sources import FILTERED_SOURCES, KNOWN_GOOD_SOURCES


class HeadlinesTest(unittest.TestCase):

    def test_sources(self) -> None:
        self.assertEqual(7, len(FILTERED_SOURCES))
        self.assertEqual(86, len(KNOWN_GOOD_SOURCES))

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
