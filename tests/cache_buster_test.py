import unittest
from urllib.parse import urlparse

from requests.models import PreparedRequest

from bboard.util.cache_buster import every


class CacheBusterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "https://example.com/foo/bar?a=1&b=2&c=3"

    def test_cache_buster(self) -> None:
        self.assertGreater(
            len(every(10, self.url)),
            len(self.url),
        )
        self.assertIn("&dojo-serial=", every(10, self.url))

    def test_urlparse(self) -> None:
        p = urlparse(self.url)
        self.assertEqual(
            "p=ParseResult(scheme='https', netloc='example.com',"
            " path='/foo/bar', params='', query='a=1&b=2&c=3', fragment='')",
            f"{p=}",
        )
        self.assertEqual(self.url, p.geturl())

    def test_prepared_request(self) -> None:
        pr = PreparedRequest()

        pr.prepare_url(self.url, {"d": 4})
        self.assertEqual("https://example.com/foo/bar?a=1&b=2&c=3&d=4", pr.url)
        pr.prepare_url(self.url, {"e": 5})
        self.assertEqual("https://example.com/foo/bar?a=1&b=2&c=3&e=5", pr.url)

        pr.prepare_url("https://example.com", {"f": 6, "g": 7})
        self.assertEqual("https://example.com/?f=6&g=7", pr.url)
