import unittest
from pprint import pp

from bboard.newsfeed.headlines import get_headlines


class HeadlinesTest(unittest.TestCase):

    def test_get_headlines(self) -> None:
        d = get_headlines()
        self.assertEqual(
            "Business Entertainment Health Science Sports Technology US World",
            " ".join(sorted(d.keys())),
        )
        print()
        sci = d["Science"]
        pp(sci)
        for article in d["Science"]:
            print(article["source"])
        print("\n\n-----------------\n\n")
        pp(d["Technology"])
