"""
Similar interface to the pypi requests library, but with caching.
"""

import datetime as dt

from requests_cache import install_cache  # pyright: ignore (reportUnknownVariableType)

from src.bboard.util.fs import temp_dir


def patch_requests_module() -> None:
    """Installs a cache for the requests package.

    This seeks to reduce the accidental harm that can come
    from a "while True:" loop which hammers a remote server,
    limiting the request rate to just three per minute.
    Explicitly use a CachedSession if you know the underlying
    API only changes at a low rate such as hourly or daily.
    """
    pass  # importing this module forced the monkey patch, and once is enough


def _patch_requests_module() -> None:
    name = f"{temp_dir()}/requests_cache.sqlite"
    lifetime = dt.timedelta(seconds=20)

    install_cache(name, expire_after=lifetime)


_patch_requests_module()
