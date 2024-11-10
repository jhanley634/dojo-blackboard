import unittest
from contextlib import suppress

from sqlalchemy.exc import IntegrityError

from bboard.transit.vehicles import (
    KEY_NAME,
    _fmt_msg,
    fmt_lat_lng,
    query_vehicles,
    store_vehicle_journeys,
)
from bboard.util.credentials import is_enabled
from bboard.util.testing import mark_slow_integration_test


class VehiclesTest(unittest.TestCase):
    @mark_slow_integration_test  # type: ignore [misc]
    def test_query_vehicles(self) -> None:
        if is_enabled(KEY_NAME):
            v = query_vehicles()
            self.assertGreater(len(str(v)), 16)  # typically 200-300 entries

    def test_formatting_helpers(self) -> None:
        self.assertEqual(
            "37.774900, -122.419400",
            fmt_lat_lng({"Latitude": "37.7749", "Longitude": "-122.4194"}),
        )

        journey = {
            "LineRef": "40",
            "DirectionRef": "N",
            "PublishedLineName": "38",
            "DestinationRef": "62035",
            "DestinationName": "Daly City",
            "VehicleLocation": {"Longitude": "-121.937492", "Latitude": "37.3535614"},
            "Bearing": None,
            "VehicleRef": "1009",
            "MonitoredCall": {
                "StopPointRef": "65541",
                "StopPointName": "Showers & Latham",
                # "DestinationDisplay": "MOUNTAIN VIEW TRANSIT CTR",
                "VehicleLocation": {
                    "Latitude": "37.7749",
                    "Longitude": "-122.4194",
                },
            },
        }
        expected = (
            "1009 N 65541 40         38                                     Daly City"
            "                                      37.353561, -121.937492"
        )
        self.assertEqual(expected, _fmt_msg(journey))

    @staticmethod
    def test_store_vehicle_journeys() -> None:
        with suppress(IntegrityError):
            store_vehicle_journeys("SC")
