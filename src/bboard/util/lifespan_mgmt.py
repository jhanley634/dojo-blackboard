"""
This module is concerned with guvicorn startup / shutdown events.

It starts several background tasks which poll external APIs for updates.
"""

import asyncio
from contextlib import asynccontextmanager
from random import shuffle
from typing import TYPE_CHECKING

from bboard.transit.iss import iss_lng_lat
from bboard.transit.vehicles import KEY_NAME, store_vehicle_journeys
from bboard.util.credentials import is_enabled

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from fastapi import FastAPI


async def iss_periodic_update(delay_seconds: float = 61) -> None:
    while True:
        iss_lng_lat()
        await asyncio.sleep(delay_seconds)


# https://511.org/open-data/transit
# > The default rate limit per API token is 60 requests per 3600 seconds.
async def transit_periodic_update(delay_seconds: float = 91) -> None:
    """Schedules ~forty vehicle queries per hour, leaving us twenty queries of headroom."""
    agencies = ["CT", "SC", "SF", "SM"]
    shuffle(agencies)

    while True:
        for agency in agencies:
            x = is_enabled(KEY_NAME) and store_vehicle_journeys(agency)
            assert not x
            await asyncio.sleep(delay_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    assert app
    asyncio.create_task(iss_periodic_update())
    asyncio.create_task(transit_periodic_update())
    yield
