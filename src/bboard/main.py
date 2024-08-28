"""
Main web server for the Blackboard application.

Routes are defined here, with the actual logic appearing in neighboring modules.

usage:  $ fastapi dev src/bboard/main.py
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.bboard.demo.greeting import greeting

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Table of contents, so folks may easily click on various endpoints."""
    html = """
    <h1>Dojo Blackboard</h1>
    <ul>
      <li><a href="hello">/hello</a></li>
    </ul>
    """
    return HTMLResponse(content=html)


@app.get("/hello")
async def hello() -> dict[str, str]:
    # We keep main.py small, delegating most endpoint logic in separate modules.
    # Please follow this pattern when adding new endpoints.
    return dict(greeting())
