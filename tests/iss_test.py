import unittest

from src.bboard.database import engine
from src.bboard.models.iss_position import Base
from src.bboard.transit.iss import iss_lng_lat

Base.metadata.create_all(engine)


class IssTest(unittest.TestCase):
    def test_iss_lng_lat(self) -> None:
        iss_lng_lat()
