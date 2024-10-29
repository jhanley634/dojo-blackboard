import unittest
from warnings import catch_warnings, simplefilter

from bboard.newsfeed.headlines import get_hash, href, store_current_articles
from bboard.newsfeed.sources import FILTERED_SOURCES, KNOWN_GOOD_SOURCES
from bboard.util.testing import mark_slow_integration_test


class HeadlinesTest(unittest.TestCase):

    def test_sources(self) -> None:
        self.assertEqual(7, len(FILTERED_SOURCES))
        self.assertEqual(86, len(KNOWN_GOOD_SOURCES))

    def test_get_hash(self) -> None:
        self.assertEqual(
            "h1cl9YXZHlk=",
            get_hash("an example title", "https://example.com"),
        )

    def test_href(self) -> None:
        self.assertEqual(
            '<a href="https://example.com">an example</a>',
            href("https://example.com", "an example"),
        )

    @mark_slow_integration_test  # type: ignore [misc]
    def test_get_headlines(self) -> None:
        with catch_warnings():
            simplefilter("ignore", category=DeprecationWarning)
            with catch_warnings():
                simplefilter("ignore", category=FutureWarning)

                self.assertGreaterEqual(store_current_articles(), 0)
