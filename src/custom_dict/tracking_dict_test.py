import unittest

from custom_dict.tracking_dict import TrackingDict


class TrackingDictTest(unittest.TestCase):
    def test_tracking_dict(self) -> None:
        d = TrackingDict()
        d["a"] = 1
        d["c"] = 3
        d["b"] = 2
        self.assertEqual([1, 3, 2], list(d.values()))
        self.assertEqual([], list(d.unread_keys()))

        d["d"] = 4
        d["e"] = 6
        d["e"] = 5
        self.assertEqual(["d", "e"], list(d.unread_keys()))
        del d["d"]
        self.assertEqual(5, d["e"])
        self.assertEqual([], list(d.unread_keys()))
