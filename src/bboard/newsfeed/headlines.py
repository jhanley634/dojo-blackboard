import datetime as dt
import json
from base64 import urlsafe_b64encode
from hashlib import sha3_224
from pprint import pp

import newspaper as news
from sqlalchemy.orm import Session

from bboard.models.headline import Headline
from bboard.util.database import get_session


def get_hash(title: str, url: str, prefix: int = 8) -> str:
    # Eight bytes offers collision resistance up to ~4 billion articles.
    digest = sha3_224(f"{title} {url}".encode()).digest()[:prefix]
    return urlsafe_b64encode(digest).decode("ascii")


def _get_article_hashes() -> set[str]:
    with get_session() as sess:
        return {a.hash for a in sess.query(Headline)}


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
headers = {"User-Agent": UA}


def href(url: str, description: str) -> str:
    return f'<a href="{url}">{description}</a>'


def store_current_articles(max_new_articles: int = 15) -> int:
    hashes = _get_article_hashes()
    num_articles = 0  # Count queries made, so we won't exceed web API rate limit.

    with get_session() as sess:
        # paper = newspaper.build("https://www.theguardian.com")
        # paper = newspaper.build("https://bbc.com")
        # paper = newspaper.build("https://cnn.com")
        paper = news.build("https://www.usatoday.com", memoize_articles=False)
        # print(paper.print_summary())
        for article in paper.articles:
            if num_articles >= max_new_articles:
                continue
            num_articles += 1

            row = _add_headline(article, sess, hashes)
            _log_article(row)

        sess.commit()
    return num_articles


def _log_article(row: dict[str, str]) -> None:
    h = row["hash"]
    with open(f"/tmp/article-{h}.txt", "w") as fout:
        json.dump(row, fout, indent=2)


def _add_headline(art: news.Article, sess: Session, hashes: set[str]) -> dict[str, str]:
    h = get_hash(art.title, art.url)
    # print("\n", art.url)
    # art.download().parse()

    row = {
        "hash": h,
        "stamp": dt.datetime.now(dt.UTC),
        "url": art.url,
        "title": art.title,
        # "content": art.text,
    }
    if h in hashes:
        pp(row)

    hashes.add(h)
    sess.add(Headline(**row))

    row["stamp"] = row["stamp"].isoformat()
    return row
