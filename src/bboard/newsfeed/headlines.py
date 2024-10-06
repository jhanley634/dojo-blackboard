import datetime as dt
import json
from base64 import urlsafe_b64encode
from hashlib import sha3_224
from pprint import pp
from typing import Any

import newspaper
from bs4 import BeautifulSoup
from newspaper.source import Category
from requests import get  # type: ignore [attr-defined]
from sqlalchemy.orm import Session

from bboard.models.article import Article
from bboard.newsfeed.sources import FILTERED_SOURCES, KNOWN_GOOD_SOURCES
from bboard.util.database import get_session

BASE_URL = "https://ok.surf/api/v1/news-feed"
KNOWN = KNOWN_GOOD_SOURCES | FILTERED_SOURCES


def _get_hash(title: str, url: str, prefix: int = 8) -> str:
    # Eight bytes offers collision resistance up to ~4 billion articles.
    digest = sha3_224(f"{title} {url}".encode()).digest()[:prefix]
    return urlsafe_b64encode(digest).decode("ascii")


def _get_article_hashes() -> set[str]:
    with get_session() as sess:
        return {a.hash for a in sess.query(Article)}


CATEGORIES_OF_INTEREST = [
    "Business",
    "Entertainment",
    "Health",
    "Science",
    "Sports",
    "Technology",
    "US",
    "World",
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
headers = {"User-Agent": UA}


def _href(url: str, description: str) -> str:
    return f'<a href="{url}">{description}</a>'


def store_current_articles(query_limit: int = 1) -> dict[str, Any]:
    hashes = _get_article_hashes()
    resp = get(BASE_URL)
    resp.raise_for_status()
    d: dict[str, Any] = json.loads(resp.text)
    num_queries = 0  # Count queries made, so we won't exceed web API rate limit.

    with get_session() as sess:
        for category in CATEGORIES_OF_INTEREST:
            for article in d[category]:
                if num_queries >= query_limit:
                    continue
                num_queries += 1

                _add_article(article, sess, hashes)

    return d


def _add_article(article: dict[str, Any], sess: Session, hashes: set[str]) -> None:
    if article["source"] not in KNOWN and False:
        src = _href(article["link"], article["source"])
        print(f'\n<p>"{src}",<p>\n')

    if article["source"][0].islower():
        article["source"] = article["source"].title()
    article["stamp"] = dt.datetime.now(dt.UTC)
    h = _get_hash(article["title"], article["link"])
    article["hash"] = h
    assert 12 == len(h)
    assert h.endswith("=")
    if h in hashes:
        return

    # resp = get(article["link"], headers=headers)
    # resp.raise_for_status()
    # content_type = resp.headers["Content-Type"]
    # assert content_type.startswith("text/html"), content_type
    publisher_link, text = _get_article_text(article["link"])
    soup = BeautifulSoup(text, "html.parser")
    # for code in soup(["script", "style"]):
    #     code.extract()
    print(soup.get_text())
    print(publisher_link)
    article["publisher_link"] = publisher_link

    hashes.add(h)

    sess.add(Article(**article))


def _get_article_text(news_article_url: str) -> tuple[str, str]:
    """Uses newspaper-4k to retrieve the text of a news article."""

    cnn_paper = newspaper.build("http://cnn.com")
    science = Category("https://www.cnn.com/science")
    assert science
    # cnn_paper.set_categories()
    # assert science in cnn_paper.categories

    print(cnn_paper.print_summary())

    paper = newspaper.build("https://www.theguardian.com")
    print(paper.print_summary())
    html = ""

    for art in cnn_paper.articles:
        print("\n\n")
        pp(art.url)
        art.download().parse()
        html = art.text

    with open("/tmp/article.html", "w") as fout:
        fout.write(html)

    return news_article_url, html
