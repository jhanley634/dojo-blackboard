# type: ignore

"""
Main web server for the Blackboard application.

Routes are defined here, with the actual logic appearing in neighboring modules.

usage:  $ fastapi dev src/bboard/main.py
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from bboard.demo.clock_display import clock_display, clock_reading
from bboard.demo.greeting import greeting
from bboard.models.iss_position import Base, IssPosition
from bboard.models.vehicle_journey import VehicleJourney
from bboard.transit.iss import iss_world_map
from bboard.transit.vehicles import query_vehicles
from bboard.util.credentials import repo_top
from bboard.util.database import engine, prune_ancient_rows
from bboard.util.lifespan_mgmt import lifespan
from bboard.util.requests import patch_requests_module
from bboard.util.web import table_of_contents

app = FastAPI(lifespan=lifespan)

assert IssPosition
assert VehicleJourney
Base.metadata.create_all(engine)
prune_ancient_rows()

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
    """Displays the current time in milliseconds."""
    return HTMLResponse(content=clock_reading())


@app.get("/transit/iss")
async def iss() -> HTMLResponse:
    """Displays current location of the International Space Station."""
    return HTMLResponse(content=iss_world_map().read_bytes(), media_type="image/png")


@app.get("/transit/vehicles")
async def vehicles() -> HTMLResponse:
    """Query the transit API for vehicle locations."""
    return HTMLResponse(content=query_vehicles().read_bytes(), media_type="image/png")


# https://hackerdojo.org/static/images/logo.png
@app.get("/favicon.ico", include_in_schema=False)
async def read_logo() -> FileResponse:
    return FileResponse(repo_top / "src/bboard/assets/logo.ico")


@app.get("/")
async def root() -> HTMLResponse:
    """A ToC that allows folks to easily click on various endpoints."""
    return HTMLResponse(content=table_of_contents(app.routes))
