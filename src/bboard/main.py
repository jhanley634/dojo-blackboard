"""
Main web server for the Blackboard application.

Routes are defined here, with the actual logic appearing in neighboring modules.

usage:  $ fastapi dev src/bboard/main.py
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.bboard.demo.greeting import greeting
from src.bboard.util.web import table_of_contents

app = FastAPI()


@app.get("/demo/hello")
async def hello() -> dict[str, str]:
    # We keep main.py small, delegating most endpoint logic in separate modules.
    # Please follow this pattern when adding new endpoints.
    return dict(greeting())


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """A ToC that allows folks to easily click on various endpoints."""
    return HTMLResponse(content=table_of_contents(app.routes))
