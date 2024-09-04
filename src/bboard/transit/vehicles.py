import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from requests import get  # type: ignore [attr-defined]

from src.bboard.util.credentials import get_api_key
from src.bboard.util.fs import temp_dir

TRANSIT = "http://api.511.org/transit"

dojo = (-122.049020, 37.3963152)  # 855 W Maude Ave, Mtn. View


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
    assert hdr["Server"] == "Microsoft-IIS/10.0"
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


def query_vehicles(agency: str = "SC") -> Path:
    # $ curl -s http://localhost:8000/transit/vehicles | jq .
    records = list(map(_fmt_msg, _get_vehicle_journey(agency)))
    assert records
    _plot_bay_area_map()
    out_file = temp_dir() / "vehicles.png"
    plt.savefig(out_file)
    return out_file


def _get_vehicle_journey(agency: str) -> Generator[dict[str, Any], None, None]:
    d = query_transit(f"{TRANSIT}/VehicleMonitoring?agency={agency}")
    svc = d["Siri"]["ServiceDelivery"]
    keys = ["ProducerRef", "ResponseTimestamp", "Status", "VehicleMonitoringDelivery"]
    assert keys == sorted(svc.keys()), svc.keys()
    assert svc["Status"]
    assert agency == svc["ProducerRef"]

    delivery = svc["VehicleMonitoringDelivery"]
    assert 3 == len(delivery.keys()), delivery.keys()
    assert "1.4" == delivery["version"]

    for record in delivery["VehicleActivity"]:
        d = dict(record["MonitoredVehicleJourney"])
        if d.get("MonitoredCall"):
            yield record["MonitoredVehicleJourney"]


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


def _plot_bay_area_map() -> None:
    plt.gca().figure.clear()
    plt.figure(figsize=(16, 12))
    m = Basemap(
        projection="merc",
        # lon_0=-122.,
        urcrnrlat=38.0,
        llcrnrlat=37.2,
        lat_ts=37.0,
        llcrnrlon=-122.6,
        urcrnrlon=-121.8,
        # resolution="h",
    )
    m.drawcoastlines()
    m.fillcontinents(color="coral", lake_color="aqua")
    m.drawcounties()
    m.drawmapscale(*dojo, *dojo, 10, barstyle="fancy")

    m.drawparallels(np.arange(30.0, 50.0, 0.1))
    m.drawmeridians(np.arange(-130.0, -110.0, 0.1))
    m.drawmapboundary(fill_color="aqua")
    plt.title("SF Bay Area")
