import unittest
from pathlib import Path

from bboard.transit.vehicles import KEY_NAME
from bboard.util.credential_env_vars import write_env_var_script
from bboard.util.credentials import file_exists, is_enabled, read_api_keys, throw
from bboard.util.fs import temp_dir


class CredentialsTest(unittest.TestCase):
    def test_creds(self) -> None:
        if is_enabled(KEY_NAME):
            d = read_api_keys()
            self.assertIn(KEY_NAME, d)

            write_env_var_script()

    def test_throw(self) -> None:
        with self.assertRaises(ValueError):  # parent of UnicodeError
            throw(UnicodeError("just exercising a helper"))

    def test_temp_dir(self) -> None:
        self.assertEqual("tmp", temp_dir().name)

    def test_file_exists(self) -> None:
        self.assertTrue(file_exists(Path()))
        self.assertIsNone(file_exists(Path("nonexistent")))
