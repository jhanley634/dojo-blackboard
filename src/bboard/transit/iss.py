"""
Tracks the current location of the International Space Station (ISS).
"""

import datetime as dt

from requests import get  # type: ignore [attr-defined]

from src.bboard.database import get_session
from src.bboard.models.iss_position import IssPosition

ISS_URL = "http://api.open-notify.org/iss-now.json"


def iss_lng_lat() -> tuple[float, float]:
    """Returns the current longitude and latitude of the ISS.

    Side effect: Writes current position to the DB.
    """
    resp = get(ISS_URL)
    resp.raise_for_status()
    j = resp.json()
    assert "success" == j["message"], j
    stamp = dt.datetime.fromtimestamp(j["timestamp"], dt.timezone.utc)
    pos = j["iss_position"]
    lng, lat = map(float, (pos["longitude"], pos["latitude"]))

    with get_session() as sess:
        sess.add(IssPosition(stamp=stamp, longitude=lng, latitude=lat))

    return lng, lat
