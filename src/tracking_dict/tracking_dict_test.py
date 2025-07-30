import unittest

from tracking_dict.tracking_dict import TrackingDict


class TrackingDictTest(unittest.TestCase):
    def test_tracking_dict(self) -> None:
        d = TrackingDict()
        d["a"] = 1
        d["c"] = 3
        d["b"] = 2

        self.assertEqual([1, 2, 3], list(d.values()))
        self.assertEqual([], list(d.unread_keys()))
