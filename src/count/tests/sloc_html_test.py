import unittest

from count.cloc import get_cloc_triple
from count.sloc import LineCounter, get_counts
from count.tests.sloc_test import _REPOS

assert get_counts


class SlocHtmlTest(unittest.TestCase):
    INCLUDE_LANGUAGES = frozenset(
        {
            ".html",
        }
    )

    def test_index_html(self) -> None:
        file = _REPOS / "llama.cpp/examples/server/public/index.html"
        cloc_cnt = get_cloc_triple(file)
        # cnt = get_counts(file)

        self.assertEqual({"blank": 31, "comment": 29, "code": 647}, cloc_cnt.__dict__)

        # self.assertEqual(cloc_cnt.__dict__, cnt.__dict__)

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
            "  <p>This is paragraph one.</p>",
            "  <p>This is paragraph two.</p>",
            "</body>",
            "</html>",
        ]
        with open("/tmp/t.html", "w") as fout:
            fout.write("\n".join([*lines, ""]))

        cnt = LineCounter(lines)
        print(cnt)
        self.assertEqual({"blank": 0, "comment": 1, "code": 11}, cnt.__dict__)
