"""
Tracks the current location of the International Space Station (ISS).
"""

from requests import get  # type: ignore [attr-defined]

ISS_URL = "http://api.open-notify.org/iss-now.json"


def iss_lng_lat() -> tuple[float, float]:
    resp = get(ISS_URL)
    resp.raise_for_status()
    j = resp.json()
    # ts = dt.datetime.fromtimestamp(j["timestamp"], dt.timezone.utc)
    assert "success" == j["message"]
    pos = j["iss_position"]
    return pos["longitude"], pos["latitude"]
