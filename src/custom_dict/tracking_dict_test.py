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

    def test_items(self) -> None:
        d = TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})
        self.assertEqual(3, d["c"])
        self.assertEqual("abd", "".join(d.unread_keys()))

        for i, (_k, _v) in enumerate(d.items()):
            if i >= 1:
                break
        self.assertEqual(["d"], list(d.unread_keys()))

    def test_update(self) -> None:
        d = TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})
        d.update({"b": 12, "x": 13, "y": 14, "z": 15})
        del d["c"]
        del d["y"]
        self.assertEqual("abdxz", "".join(d.unread_keys()))

    def test_union(self) -> None:
        """Same as test_update(), pretty much."""
        d1 = TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})
        d = d1 | {"b": 12, "x": 13, "y": 14, "z": 15}
        del d["c"]
        del d["y"]
        self.assertEqual("abdxz", "".join(d.unread_keys()))

    def test_popitem(self) -> None:
        d = TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})
        self.assertEqual(("a", 1), d.popitem())
        self.assertEqual(("b", 2), d.popitem())
        self.assertEqual("cd", "".join(d.unread_keys()))

        self.assertEqual(3, d.pop("c"))
        self.assertEqual("d", "".join(d.unread_keys()))

    def test_copy(self) -> None:
        d1 = TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})
        d = d1.copy()
        self.assertEqual("", "".join(d1.unread_keys()))
        self.assertEqual("abcd", "".join(d.unread_keys()))
