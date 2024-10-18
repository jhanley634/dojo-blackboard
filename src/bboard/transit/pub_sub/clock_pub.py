#! /usr/bin/env python
"""
Publish a clock's 1 Hz  "tick" messages.
"""

import json
from time import sleep, time

from pynng import Pub0

PUB_SUB_URL = "tcp://localhost:2100"
TOPIC = b"1"


def publish(hz: float = 1.0) -> None:
    with Pub0(listen=PUB_SUB_URL) as sock:
        while True:
            d = {"time": round(time(), 3)}
            sock.send(TOPIC + json.dumps(d).encode())
            sleep(1.0 / hz)


if __name__ == "__main__":
    publish()
