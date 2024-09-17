import unittest

from starlette.routing import Route

from bboard.util.web import table_of_contents


class WebTest(unittest.TestCase):
    def test_toc(self) -> None:
        route = Route("/foo", str.split, methods=["GET"])
        suffix = "     /foo\n    </a>\n   </li>\n  </ul>\n </body>\n</html>\n"
        self.assertTrue(table_of_contents([route]).endswith(suffix))
