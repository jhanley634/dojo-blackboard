#! /usr/bin/env python
"""
Subscribe to "tick" messages.
"""
import json
from time import time

from pynng import Sub0

from src.bboard.transit.clock_pub import PUB_SUB_URL


def subscribe() -> None:
    with Sub0(dial=PUB_SUB_URL) as sock:
        sock.subscribe(b"")  # pyright: ignore (reportUnknownMemberType)
        while True:
            msg: bytes = sock.recv()
            d: dict[str, float] = json.loads(msg)
            print(time() - d["time"])


if __name__ == "__main__":
    subscribe()
