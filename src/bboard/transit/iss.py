"""
Tracks the current location of the International Space Station (ISS).
"""

import datetime as dt
from collections.abc import Generator
from pathlib import Path
from typing import Any

import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from requests import get  # type: ignore [attr-defined]

from bboard.models.iss_position import IssPosition
from bboard.util.cache_buster import every
from bboard.util.database import get_session
from bboard.util.fs import temp_dir

matplotlib.use("Agg")

ISS_URL = "http://api.open-notify.org/iss-now.json"


def iss_lng_lat() -> tuple[float, float]:
    """Returns the current longitude and latitude of the ISS.

    Side effect: Writes current position to the DB.
    """
    resp = get(every(60, ISS_URL))
    resp.raise_for_status()
    j = resp.json()
    assert "success" == j["message"], j
    stamp = dt.datetime.fromtimestamp(j["timestamp"], dt.UTC)
    pos = j["iss_position"]
    lng, lat = map(float, (pos["longitude"], pos["latitude"]))

    with get_session() as sess:
        recent = sess.query(IssPosition).order_by(IssPosition.stamp.desc()).first()
        row: dict[str, Any] = {"stamp": stamp, "longitude": lng, "latitude": lat}
        assert repr(recent)
        if recent is None or recent.stamp < stamp:
            # Wait twenty seconds for cache TTL, and the next line _will_ be covered.
            sess.add(IssPosition(**row))  # pragma: no cover

    return lng, lat


def get_iss_breadcrumbs(limit: int) -> Generator[tuple[float, float]]:
    with get_session() as sess:
        for row in sess.query(IssPosition).order_by(IssPosition.stamp.desc()).limit(limit):
            yield row.longitude, row.latitude


def _get_world_map() -> Basemap:
    plt.clf()
    plt.figure(figsize=(16, 12))
    m = Basemap(projection="robin", lon_0=0.0)
    m.drawcoastlines()
    m.fillcontinents(color="lavender", lake_color="aqua")
    pastel_aqua = "#D5F6FB"
    m.drawmapboundary(fill_color=pastel_aqua)
    return m


def iss_world_map(num_crumbs: int = 50) -> Path:
    """Returns a world map depicting recent ISS breadcrumbs."""
    lng, lat = iss_lng_lat()
    m = _get_world_map()
    crumbs = list(get_iss_breadcrumbs(num_crumbs))
    for i, (lng, lat) in enumerate(reversed(crumbs)):
        color = mpl.colormaps["Blues"](int(256 * i / len(crumbs)))
        m.plot(*m(lng, lat), "+", color=color, markersize=6)
    x, y = map(float, m(lng, lat))  # pyright: ignore (reportArgumentType)
    plt.axvline(x=x, color="gray", linestyle="--")  # highlight the most recent position
    plt.axhline(y=y, color="gray", linestyle="--")
    plt.savefig(out_file := Path(temp_dir() / "iss_map.png"))
    return out_file
