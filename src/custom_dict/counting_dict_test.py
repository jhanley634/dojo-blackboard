import unittest

from custom_dict.counting_dict import AccessCounterDict
from custom_dict.tracking_dict_test import _example_mapping


class AccessCounterDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.d = AccessCounterDict(dict(_example_mapping()))

    def test_access_counter_dict(self) -> None:
        d = self.d.copy()
        self.assertEqual(4, len(d))
        self.assertEqual(5, d["b"] + d["c"])
        self.assertEqual(0, len(d.count))
