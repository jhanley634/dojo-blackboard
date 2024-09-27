import unittest

from bboard.newsfeed.headlines import store_current_articles


class HeadlinesTest(unittest.TestCase):

    def test_get_headlines(self) -> None:
        d = store_current_articles()
        self.assertEqual(
            "Business Entertainment Health Science Sports Technology US World",
            " ".join(sorted(d.keys())),
        )
        expected_keys = "hash, host, link, og, source, source_icon, stamp, title"
        for section in ["Science", "Technology"]:
            for article in d[section]:
                self.assertEqual(expected_keys, ", ".join(sorted(article.keys())))
