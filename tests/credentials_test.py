import unittest

from src.bboard.util.credentials import read_api_keys, throw


class CredentialsTest(unittest.TestCase):
    def test_creds(self) -> None:
        df = read_api_keys()
        self.assertEqual(
            "key_name github_user added expires key_value".split(),
            df.columns.tolist(),
        )
        self.assertGreaterEqual(len(df), 2)

    def test_throw(self) -> None:
        with self.assertRaises(ValueError):  # parent of UnicodeError
            throw(UnicodeError("just exercising a helper"))
