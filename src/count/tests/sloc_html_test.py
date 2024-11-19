import unittest

from bboard.util.testing import mark_slow_integration_test
from count.cloc import get_cloc_triple
from count.sloc import XmlLineCounter, get_counts
from count.tests.sloc_test import _REPOS

assert get_counts


class SlocHtmlTest(unittest.TestCase):
    INCLUDE_LANGUAGES = frozenset(
        {
            ".htm",
            ".html",
            ".xml",
        }
    )

    @mark_slow_integration_test  # type: ignore [misc]
    def test_html_files(self) -> None:
        for file in _REPOS.glob("**/*"):
            if file.suffix not in self.INCLUDE_LANGUAGES:
                continue
            cnt = get_counts(file)
            self.assertTrue(cnt.__dict__)

            cloc_cnt = get_cloc_triple(file)
            cnt = get_counts(file)
            self.assertEqual(cloc_cnt.__dict__, cnt.__dict__)

    def test_html(self) -> None:
        lines = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "  <title>Page Title</title>",
            "</head>",
            "<body>",
            "  <!-- brief comment -->",
            "  <h1>This is a Heading</h1>",
            "  <!-- multi-line comment",
            "  <p>This is paragraph one.</p>",
            "  <p>This is paragraph two.</p>",
            "  end of comment -->",
            "</body>",
            "</html>",
        ]
        cnt = XmlLineCounter(lines)
        self.assertEqual({"blank": 0, "comment": 5, "code": 9}, cnt.__dict__)
