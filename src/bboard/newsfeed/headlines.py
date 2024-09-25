import json
from typing import Any

from requests import get  # type: ignore [attr-defined]

BASE_URL = "https://ok.surf/api/v1/news-feed"


def get_headlines() -> dict[str, Any]:
    resp = get(BASE_URL)
    resp.raise_for_status()
    d: dict[str, Any] = json.loads(resp.text)
    for category in ["Science", "Technology"]:
        for article in d[category]:
            if article["source"][0].islower():
                article["source"] = article["source"].title()
    return d
