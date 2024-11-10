import unittest

from bboard.util.database import prune_ancient_rows


class DatabaseTest(unittest.TestCase):

    @staticmethod
    def test_prune_ancient_rows() -> None:
        prune_ancient_rows()
