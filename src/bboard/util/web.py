"""
Web helpers.
"""

from bs4 import BeautifulSoup
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute, Route


def aref(url: str, description: str = "") -> str:
    """Return an HTML anchor tag."""
    description = description or url
    return f'<a href="{url}">{description}</a>'


def table_of_contents(app_routes: list[BaseRoute]) -> str:
    """Return an HTML table of contents for the given FastAPI app."""
    html = """<!DOCTYPE html><html lang="en">
    <head><title>Dojo Blackboard</title></head>
    <body><h1>Dojo Blackboard</h1>
    <ul>
    """
    endpoints = sorted(
        r.path
        for r in app_routes
        if isinstance(r, (Route, APIRoute))
        and len(r.path) > 1
        and r.path != "/docs/oauth2-redirect"
        and "GET" in (r.methods or [])
    )
    soup = BeautifulSoup(
        html + "".join(f"<li>{aref(url)}</li>" for url in endpoints),
        "html.parser",
    )
    return str(soup.prettify())
