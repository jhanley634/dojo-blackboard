"""
This module is concerned with guvicorn startup / shutdown events.

It starts several background tasks which poll external APIs for updates.
"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from random import shuffle

from fastapi import FastAPI

from bboard.transit.iss import iss_lng_lat
from bboard.transit.vehicles import store_vehicle_journeys


async def iss_periodic_update(delay_seconds: float = 31) -> None:
    while True:
        iss_lng_lat()
        await asyncio.sleep(delay_seconds)


async def transit_periodic_update(delay_seconds: float = 61) -> None:
    agencies = ["SC", "SF", "SM", "CT"]
    shuffle(agencies)

    while True:
        for agency in agencies:
            store_vehicle_journeys(agency)
            await asyncio.sleep(delay_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    assert app
    asyncio.create_task(iss_periodic_update())
    asyncio.create_task(transit_periodic_update())
    yield
