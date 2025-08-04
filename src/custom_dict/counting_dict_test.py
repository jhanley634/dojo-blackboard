import unittest

from custom_dict.counting_dict import AccessCounterDict


class AccessCounterDictTest(unittest.TestCase):
    def test_access_counter_dict(self) -> None:
        d = AccessCounterDict({"a": 1, "b": 2})
        assert d
