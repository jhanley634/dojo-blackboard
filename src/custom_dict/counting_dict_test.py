import unittest
from copy import deepcopy

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

    def test_update(self) -> None:
        d = self.d.copy()
        d.update({"b": 12, "x": 13, "y": 14, "z": 15})
        del d["c"]
        del d["y"]
        self.assertEqual("abdxz", "".join(d.unread_keys()))

    def test_deepcopy(self) -> None:
        d1 = self.d.copy()
        d = deepcopy(d1)
        self.assertEqual("", "".join(d1.unread_keys()))

        self.assertEqual(3, d["c"])
        self.assertEqual("abd", "".join(d.unread_keys()))
