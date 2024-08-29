import unittest

from src.bboard.transit.vehicles import query_vehicles


class VehiclesTest(unittest.TestCase):
    def test_query_vehicles(self) -> None:
        v = query_vehicles()
        self.assertGreater(len(v), 20)  # typically 200-300
