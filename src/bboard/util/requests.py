"""
Similar interface to the pypi requests library, but with caching.
"""

import datetime as dt

from requests_cache import install_cache  # pyright: ignore (reportUnknownVariableType)

from bboard.util.fs import temp_dir


def patch_requests_module() -> None:
    """Installs a cache for the requests package.

    This seeks to reduce the accidental harm that can come
    from a "while True:" loop which hammers a remote server,
    limiting the request rate to one every six minutes.
    Explicitly use a CachedSession if you know the underlying
    API only changes at a lower rate such as hourly or daily.
    Explicitly use a cache-busting every() for faster updates.
    """
    return  # importing this module forced the monkey patch, and once is enough


def _patch_requests_module() -> None:
    name = f"{temp_dir()}/requests_cache.sqlite"
    epsilon = dt.timedelta(seconds=0.200)  # 1% -- most GETs complete within a quarter second

    # four agencies, with query issued every ~90 seconds
    lifetime = dt.timedelta(minutes=6) - epsilon

    install_cache(name, expire_after=lifetime)


_patch_requests_module()
