import unittest

from bboard.newsfeed.headlines import get_headlines


class HeadlinesTest(unittest.TestCase):

    def test_get_headlines(self) -> None:
        d = get_headlines()
        self.assertEqual(
            "Business Entertainment Health Science Sports Technology US World",
            " ".join(sorted(d.keys())),
        )
        expected_keys = "link, og, source, source_icon, title"
        for section in ["Science", "Technology"]:
            for article in d[section]:
                self.assertEqual(expected_keys, ", ".join(sorted(article.keys())))
