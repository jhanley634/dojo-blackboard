import unittest

from bboard.util.testing import mark_slow_integration_test
from count.cloc import get_cloc_triple
from count.sloc import XML_LANGUAGES, XmlLineCounter, get_counts
from count.tests.sloc_test import _REPOS, TestCloc

assert get_counts


class SlocHtmlTest(unittest.TestCase):

    @mark_slow_integration_test  # type: ignore [misc]
    def ztest_xml_files(self) -> None:
        for file in _REPOS.glob("**/*"):
            sup_lang = set(TestCloc.SUPPORTED_LANGUAGES)
            if file.suffix in XML_LANGUAGES | sup_lang:
                print(file.suffix, "\t", file)
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

    def test_php(self) -> None:
        lines = [
            "<?php",  # No, cloc does not view this as a shebang.
            "x = 1;",
        ]
        cnt = XmlLineCounter(lines)
        self.assertEqual({"blank": 0, "comment": 0, "code": 2}, cnt.__dict__)

        lines = [
            "class Authenticate extends Middleware",
            "{",
            "    /**",
            "     * Get the path the user should be redirected to when they are not authenticated.",
            "     *",
            r"     * @param  \Illuminate\Http\Request  $request",
            "     * @return string|null",
            "     */",
            "    protected function redirectTo($request)",
        ]
        cnt = XmlLineCounter(lines)
        assert cnt.blank == 0
        # self.assertEqual({"blank": 0, "comment": 6, "code": 3}, cnt.__dict__)
