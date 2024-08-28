import unittest
from time import sleep, time

from requests import get  # type: ignore [attr-defined]

from src.bboard.util.requests import patch_requests_module


class RequestsTest(unittest.TestCase):
    def test_space_station(self) -> None:
        """Verifies that a get() can produce "stale" results, due to caching."""
        patch_requests_module()
        while True:
            url = "http://api.open-notify.org/iss-now.json"
            resp = get(url)
            resp.raise_for_status()
            sleep(0.005)
            j = resp.json()
            self.assertEqual("success", j["message"])
            self.assertEqual(
                "longitude, latitude",
                ", ".join(j["iss_position"].keys()),
            )
            # post-condition: the retrieved timestamp shall be at least 1 second old
            if int(time()) > j["timestamp"] + 1:
                break
