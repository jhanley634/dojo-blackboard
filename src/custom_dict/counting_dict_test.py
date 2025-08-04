import unittest

from custom_dict.counting_dict import AccessCounterDict
from custom_dict.tracking_dict_test import _example_mapping


class AccessCounterDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.d = AccessCounterDict(dict(_example_mapping()))

    def test_access_counter_dict(self) -> None:
        d = self.d.copy()
        self.assertEqual(4, len(d))

        self.assertEqual(0, len(d.count))
        self.assertEqual(5, d["b"] + d["c"])
        self.assertEqual(2, len(d.count))

        d.reset_counts()
        self.assertEqual(0, len(d.count))
        self.assertEqual(5, d.get("b", 0) + d.get("c"))
        self.assertEqual(2, len(d.count))

    def test_get_count(self) -> None:
        d = self.d.copy()

        self.assertEqual(0, d.get_count("z"))
        d["z"] = 26
        self.assertEqual(0, d.get_count("z"))  # we count reads, not writes

        for i in range(12):
            self.assertEqual(i, d.get_count("d"))
            self.assertEqual(4, d["d"])

        d.reset_counts()
        self.assertEqual(0, d.get_count("d"))
