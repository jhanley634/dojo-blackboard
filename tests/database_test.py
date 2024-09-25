import unittest

from bboard.util.database import prune_ancient_rows


class DatabaseTest(unittest.TestCase):

    def test_prune_ancient_rows(self) -> None:
        prune_ancient_rows()
