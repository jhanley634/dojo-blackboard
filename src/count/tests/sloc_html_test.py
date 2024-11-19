import unittest

from count.bisect import TEMP
from count.cloc import get_cloc_triple
from count.sloc import XmlLineCounter, get_counts
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
        lines = file.read_text().splitlines()

        for i in range(274, 1000, 1):
            temp_file = TEMP / "t.html"
            TEMP.mkdir(exist_ok=True)
            with open(temp_file, "w") as fout:
                fout.write("\n".join([*lines[:i], ""]))

            cloc_cnt = get_cloc_triple(temp_file)
            cnt = get_counts(temp_file)

            # self.assertEqual({"blank": 31, "comment": 29, "code": 647}, cloc_cnt.__dict__)

            print(i)
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
        with open("/tmp/t.html", "w") as fout:
            fout.write("\n".join([*lines, ""]))

        cnt = XmlLineCounter(lines)
        self.assertEqual({"blank": 0, "comment": 5, "code": 9}, cnt.__dict__)
