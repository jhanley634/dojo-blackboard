import json
import os
from collections.abc import Generator
from typing import Any

from requests import get  # type: ignore [attr-defined]

TRANSIT = "http://api.511.org/transit"


def query_transit(url: str) -> dict[str, Any]:
    """Given a URL with no credential, returns an API result."""
    assert "?" in url, url
    api_key = os.environ["KEY511"]
    url += f"&api_key={api_key}"
    resp = get(url)
    resp.raise_for_status()
    bom = "\ufeff"
    hdr = resp.headers
    assert hdr["Content-Type"] == "application/json; charset=utf-8"
    assert hdr["Server"] == "Microsoft-IIS/10.0"
    assert resp.text.startswith(bom)  # Grrr. Gee, thanks, μsoft!
    d = json.loads(resp.text.lstrip(bom))
    assert isinstance(d, dict), d
    return d


def fmt_lat_lng(location: dict[str, str]) -> str:
    latitude = location["Latitude"] or "0.0"
    longitude = location["Longitude"] or "0.0"
    lat, lng = map(float, (latitude, longitude))
    return f"{lat:.6f}, {lng:.6f}"


def query_vehicles(agency: str = "SC") -> list[str]:
    # $ curl -s http://localhost:8000/transit/vehicles | jq .
    records = list(map(_fmt_msg, _get_vehicle_journey(agency)))
    return records


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
