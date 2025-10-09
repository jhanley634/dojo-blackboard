import io
import pickle  # nosec
import unittest
from copy import deepcopy
from pathlib import Path

from custom_dict.counting_dict import AccessCounterDict
from custom_dict.tracking_dict import TrackingDict


def example_mapping() -> TrackingDict:
    return TrackingDict({"a": 1, "b": 2, "c": 3, "d": 4})


def unread_keys(d: TrackingDict | AccessCounterDict) -> str:
    """
    Returns blank delimited unread keys.

    The result will be ambiguous if your keys contain SPACE characters.
    """
    return " ".join(map(str, d.unread_keys()))


class TrackingDictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.d = example_mapping()

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
        self.assertEqual("d e", unread_keys(d))
        del d["d"]
        self.assertEqual(5, d["e"])
        self.assertEqual([], list(d.unread_keys()))

    def test_items(self) -> None:
        d = self.d.copy()
        self.assertEqual(3, d["c"])
        self.assertEqual("a b d", unread_keys(d))

        for i, (_k, _v) in enumerate(d.items()):
            if i >= 1:
                break
        self.assertEqual("d", unread_keys(d))

    def test_update(self) -> None:
        d = self.d.copy()
        d.update({"b": 12, "x": 13, "y": 14, "z": 15})
        del d["c"]
        del d["y"]
        self.assertEqual("a b d x z", unread_keys(d))

    def test_union(self) -> None:
        """Same as test_update(), pretty much."""
        d1 = self.d.copy()
        d = d1 | {"b": 12, "x": 13, "y": 14, "z": 15}
        del d["c"]
        del d["y"]
        self.assertEqual("a b d x z", unread_keys(d))

    def test_popitem(self) -> None:
        d = self.d.copy()
        self.assertEqual(("a", 1), d.popitem())
        self.assertEqual(("b", 2), d.popitem())
        self.assertEqual("c d", unread_keys(d))

        self.assertEqual(3, d.pop("c"))
        self.assertEqual("d", unread_keys(d))

    def test_copy(self) -> None:
        d1 = self.d.copy()
        d = d1.copy()
        self.assertEqual("", unread_keys(d1))
        self.assertEqual("a b c d", unread_keys(d))

    def test_deepcopy(self) -> None:
        d1 = self.d.copy()
        d = deepcopy(d1)
        self.assertEqual("", unread_keys(d1))

        self.assertEqual(3, d["c"])
        self.assertEqual("a b d", unread_keys(d))

    def test_tuple_keys(self) -> None:
        d = TrackingDict({(5, 57): "a", (5, 59): "b", (7, 59): "c"})
        self.assertEqual("b", d[(5, 59)])
        self.assertEqual("(5, 57) (7, 59)", unread_keys(d))


class TrackingDictPickleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.d = example_mapping()

    def test_pickle_roundtrip_with_filesystem(self) -> None:
        d = self.d.copy()
        self.assertEqual(3, d["c"])
        pkl = Path("/tmp/dict.pkl")
        with open(pkl, "wb") as f:
            pickle.dump(d, f)

        with open(pkl, "rb") as f:
            d1 = pickle.load(f)  # nosec
        pkl.unlink()

        self._verify_equality(d, d1)

    def test_pickle_roundtrip_with_bytesio(self) -> None:
        d = self.d.copy()
        self.assertEqual(3, d["c"])
        buf = io.BytesIO()
        pickle.dump(d, buf)
        buf.seek(0)

        d1 = pickle.load(buf)  # nosec

        self._verify_equality(d, d1)

    def _verify_equality(self, d: TrackingDict, d1: TrackingDict) -> None:
        self.assertEqual(list(d.unread_keys()), list(d1.unread_keys()))
        self.assertEqual(d.used, d1.used)
        self.assertEqual(d.data, d1.data)
        self.assertEqual(d, d1)
