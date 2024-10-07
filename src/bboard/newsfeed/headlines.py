import datetime as dt
import json
from base64 import urlsafe_b64encode
from hashlib import sha3_224
from pprint import pp

import newspaper as news
from sqlalchemy.orm import Session

from bboard.models.article import Article
from bboard.util.database import get_session


def _get_hash(title: str, url: str, prefix: int = 8) -> str:
    # Eight bytes offers collision resistance up to ~4 billion articles.
    digest = sha3_224(f"{title} {url}".encode()).digest()[:prefix]
    return urlsafe_b64encode(digest).decode("ascii")


def _get_article_hashes() -> set[str]:
    with get_session() as sess:
        return {a.hash for a in sess.query(Article)}


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0"
headers = {"User-Agent": UA}


def _href(url: str, description: str) -> str:
    return f'<a href="{url}">{description}</a>'


def store_current_articles(max_new_articles: int = 15) -> int:
    hashes = _get_article_hashes()
    num_articles = 0  # Count queries made, so we won't exceed web API rate limit.

    with get_session() as sess:
        # paper = newspaper.build("https://www.theguardian.com")
        # paper = newspaper.build("https://bbc.com")
        # paper = newspaper.build("https://cnn.com")
        paper = news.build("https://www.usatoday.com", memoize_articles=False)
        print(paper.print_summary())
        for article in paper.articles:
            if num_articles >= max_new_articles:
                continue
            num_articles += 1

            _add_article(article, sess, hashes)

        sess.commit()
    return num_articles


def _add_article(art: news.Article, sess: Session, hashes: set[str]) -> None:
    print("\n", art.url)
    art.download().parse()

    row = {
        "hash": _get_hash(art.title, art.url),
        "stamp": dt.datetime.now(dt.UTC),
        "url": art.url,
        "title": art.title,
        "content": art.text,
    }
    if row["hash"] in hashes:
        pp(row)

    hashes.add(row["hash"])
    sess.add(Article(**row))

    row["stamp"] = row["stamp"].isoformat()
    h = row["hash"]
    with open(f"/tmp/article-{h}.txt", "w") as fout:
        fout.write(json.dumps(row, indent=2))
        fout.write("\n\n========\n\n")
        fout.write(row["content"])
