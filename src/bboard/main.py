"""
Main web server for the Blackboard application.

Routes are defined here, with the actual logic appearing in neighboring modules.

usage:  $ fastapi dev src/bboard/main.py
"""

import datetime as dt

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.bboard.database import engine
from src.bboard.demo.clock_display import clock_display
from src.bboard.demo.greeting import greeting
from src.bboard.models.iss_position import Base, IssPosition
from src.bboard.transit.iss import iss_lng_lat
from src.bboard.transit.vehicles import query_vehicles
from src.bboard.util.requests import patch_requests_module
from src.bboard.util.web import table_of_contents

app = FastAPI()

assert IssPosition
Base.metadata.create_all(engine)


patch_requests_module()


@app.get("/demo/hello")
async def hello() -> dict[str, str]:
    # We keep main.py small, delegating most endpoint logic to companion modules.
    # Please follow this pattern when adding new endpoints.
    return dict(greeting())


@app.get("/transit/clock")
async def clock() -> HTMLResponse:
    """Demonstrates 1 Hz screen updates."""
    return HTMLResponse(content=str(clock_display()))


@app.get("/transit/clock-value")
async def clock_value() -> HTMLResponse:
    """Displays the current time."""
    now = dt.datetime.now().isoformat(sep=" ")
    return HTMLResponse(content=now)


@app.get("/transit/iss")
async def iss() -> tuple[float, float]:
    """Gives current location of the International Space Station."""
    lng, lat = iss_lng_lat()
    return lng, lat


@app.get("/transit/vehicles")
async def vehicles() -> list[str]:
    """Query the transit API for vehicle locations."""
    return sorted(query_vehicles())


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """A ToC that allows folks to easily click on various endpoints."""
    return HTMLResponse(content=table_of_contents(app.routes))
