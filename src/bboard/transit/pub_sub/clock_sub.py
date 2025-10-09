#! /usr/bin/env python
"""
Subscribe to "tick" messages.
"""

import json
from pprint import pp
from time import time
from typing import TYPE_CHECKING

from pynng import Sub0

from bboard.transit.pub_sub.clock_pub import PUB_SUB_URL, TOPIC

if TYPE_CHECKING:
    from collections.abc import Generator


def subscribe(num_messages: int = 6) -> Generator[float]:
    with Sub0(dial=PUB_SUB_URL) as sock:
        sock.subscribe(TOPIC)
        for _ in range(num_messages):
            msg: bytes = sock.recv()
            d: dict[str, float] = json.loads(msg[len(TOPIC) :])
            yield time() - d["time"]


if __name__ == "__main__":
    pp(list(subscribe()))
