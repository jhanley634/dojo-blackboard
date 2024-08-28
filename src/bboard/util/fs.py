"""
Filesystem helpers.
"""

from os import W_OK, access, getenv
from pathlib import Path

from src.bboard.util.credentials import throw

repo_top = Path(__file__).resolve().parents[3]


def temp_dir() -> Path:
    """Returns a writable temporary directory, for caches and reporting output.

    Creating a temp file which persists after the python interpreter exits
    can be a handy aid to debugging.

    You should instead prefer `tempfile.TemporaryDirectory()` if it's desirable
    to have temp output cleaned up automatically. One use case would be
    asking matplotlib to produce a chart.png which is sent on port 80
    and then deleted.
    """
    d = Path(getenv("TEMP_DIR") or "/tmp")
    diagnostic = f"Please set the TEMP_DIR env var to a writable directory: {d}"
    is_usable = d.is_dir() and access(d, W_OK)
    is_usable or throw(FileNotFoundError(diagnostic))

    return d
