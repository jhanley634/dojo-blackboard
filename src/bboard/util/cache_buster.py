from time import time

from requests.models import PreparedRequest


def every(
    seconds: float = 60,
    url: str = "https://example.com",
    serial_name: str = "dojo-serial",
) -> str:
    """Tacks on a cache-busting serial / timestamp to force faster updates
    than what _patch_requests_module would ordinarily allow.
    """
    now = int(time() / seconds)  # By default, this ticks once per minute.
    pr = PreparedRequest()
    pr.prepare_url(url, params={serial_name: now})
    return f"{pr.url}"
