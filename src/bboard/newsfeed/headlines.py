import datetime as dt
import json
from base64 import b64encode
from hashlib import sha3_224
from typing import Any
from urllib.parse import urlparse

from requests import get  # type: ignore [attr-defined]

from bboard.models.article import Article
from bboard.util.database import get_session

BASE_URL = "https://ok.surf/api/v1/news-feed"


def _get_hash(title: str, url: str, prefix: int = 8) -> str:
    # Eight bytes offers collision resistance up to ~4 billion articles.
    digest = sha3_224(f"{title} {url}".encode()).digest()[:prefix]
    return b64encode(digest).decode("ascii")


def _get_article_hashes() -> set[str]:
    with get_session() as sess:
        return {a.hash for a in sess.query(Article)}


def store_current_articles() -> dict[str, Any]:
    hashes = _get_article_hashes()
    resp = get(BASE_URL)
    resp.raise_for_status()
    d: dict[str, Any] = json.loads(resp.text)

    with get_session() as sess:
        sess.query(Article).delete()
        for category in ["Science", "Technology"]:
            for article in d[category]:
                if article["source"][0].islower():
                    article["source"] = article["source"].title()
                article["stamp"] = dt.datetime.now(dt.UTC)
                h = _get_hash(article["title"], article["link"])
                article["hash"] = h
                assert 12 == len(h)
                assert h.endswith("=")
                if h in hashes:
                    continue
                p = urlparse(article["link"])
                article["host"] = p.netloc

                sess.add(Article(**article))

    return d
