import datetime as dt
import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from requests import get  # type: ignore [attr-defined]

from bboard.database import get_session
from bboard.models.vehicle_journey import VehicleJourney
from bboard.util.credentials import get_api_key
from bboard.util.fs import temp_dir

matplotlib.use("Agg")

KEY_NAME = "TRANSIT_KEY"
TRANSIT = "http://api.511.org/transit"

dojo = (-122.049020, 37.3963152)  # 855 W Maude Ave, Mtn. View
scale = (-122.115, 37.16)


def query_transit(url: str) -> dict[str, Any]:
    """Given a URL with no credential, returns an API result."""
    assert "?" in url, url
    api_key = get_api_key("TRANSIT_KEY")
    url += f"&api_key={api_key}"
    resp = get(url)
    resp.raise_for_status()
    bom = "\ufeff"
    hdr = resp.headers
    assert hdr["Content-Type"] == "application/json; charset=utf-8"
    assert hdr["Server"].startswith("Microsoft-IIS/")
    assert resp.text.startswith(bom)  # Grrr. Gee, thanks, μsoft!
    d: dict[str, Any] = json.loads(resp.text.lstrip(bom))
    assert isinstance(d, dict), d
    assert all(isinstance(k, str) for k in d), d
    return d


def fmt_lat_lng(location: dict[str, str]) -> str:
    latitude = location["Latitude"] or "0.0"
    longitude = location["Longitude"] or "0.0"
    lat, lng = map(float, (latitude, longitude))
    return f"{lat:.6f}, {lng:.6f}"


def query_vehicles() -> Path:
    m = _plot_bay_area_map()
    for agency in ["SC", "SF", "SM", "CT"]:
        plot_agency_vehicles(m, agency)

    out_file = Path(temp_dir() / "vehicles.png")
    plt.savefig(out_file)
    return out_file


def plot_agency_vehicles(m: Basemap, agency: str = "SC") -> None:
    color = "lime" if agency == "CT" else "blue"

    for row in get_recent_vehicle_journeys(agency):
        lng, lat = row.longitude, row.latitude
        m.plot(*m(lng, lat), "+", color=color, markersize=6)


def get_recent_vehicle_journeys(
    agency: str, limit: int = 6
) -> Generator[VehicleJourney, None, None]:
    with get_session() as sess:
        for row in (
            sess.query(VehicleJourney)
            .filter(VehicleJourney.agency == agency)
            .order_by(VehicleJourney.stamp.desc())
            .limit(limit)
            .all()
        ):
            yield row


def store_vehicle_journeys(agency: str) -> None:
    d = query_transit(f"{TRANSIT}/VehicleMonitoring?agency={agency}")
    svc = d["Siri"]["ServiceDelivery"]
    keys = ["ProducerRef", "ResponseTimestamp", "Status", "VehicleMonitoringDelivery"]
    assert keys == sorted(svc.keys()), svc.keys()
    assert svc["Status"]
    assert agency == svc["ProducerRef"]

    delivery = svc["VehicleMonitoringDelivery"]
    assert 3 == len(delivery.keys()), delivery.keys()
    assert "1.4" == delivery["version"]

    with get_session() as sess:
        for record in delivery["VehicleActivity"]:
            stamp = dt.datetime.fromisoformat(record["RecordedAtTime"])
            d = dict(record["MonitoredVehicleJourney"])
            if d.get("MonitoredCall"):
                loc = d["VehicleLocation"]
                row: dict[str, Any] = {
                    "stamp": stamp,
                    "agency": agency,
                    "vehicle_ref": d["VehicleRef"],
                    "longitude": float(loc["Longitude"]),
                    "latitude": float(loc["Latitude"]),
                }
                sess.add(VehicleJourney(**row))

                # yield record["MonitoredVehicleJourney"]
                # record["Bearing"] is float or None
                # print(lng, lat, record["VehicleRef"], ",", record["PublishedLineName"])


def _fmt_msg(journey: dict[str, Any], width: int = 38) -> str:
    pad = " " * width
    call = journey["MonitoredCall"]
    return " ".join(
        [
            journey["VehicleRef"],
            (journey["DirectionRef"] or "-"),
            call["StopPointRef"],  # cf StopPointName
            (journey.get("LineRef") or "-").ljust(10),
            ((journey.get("PublishedLineName") or "-") + pad)[:width],
            (journey["DestinationName"] or "-").ljust(46),
            fmt_lat_lng(journey["VehicleLocation"]),
        ]
    )


def _plot_bay_area_map() -> Basemap:
    plt.clf()
    plt.figure(figsize=(16, 12))
    m = Basemap(
        projection="merc",
        # lon_0=-122.,
        urcrnrlat=38.0,
        llcrnrlat=37.1,
        lat_ts=37.0,
        llcrnrlon=-122.6,
        urcrnrlon=-121.7,
        resolution="i",
    )
    m.drawcoastlines()
    m.fillcontinents(color="coral", lake_color="aqua")
    m.drawcounties()
    m.drawmapscale(*scale, *scale, 10, barstyle="fancy")
    m.plot(*m(*dojo), "r*", markersize=12)

    m.drawparallels(np.arange(30.0, 50.0, 0.1))
    m.drawmeridians(np.arange(-130.0, -110.0, 0.1))
    m.drawmapboundary(fill_color="aqua")
    plt.title("SF Bay Area")
    return m
