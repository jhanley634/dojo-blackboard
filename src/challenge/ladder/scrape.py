import re
from collections.abc import Generator
from pprint import pp

from bs4 import BeautifulSoup

from challenge.ladder.lexicon import cached_session


def _get_page() -> BeautifulSoup:
    url = "http://datagenetics.com/blog/april32019/"
    resp = cached_session().get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def scrape_long_ladders() -> Generator[list[str]]:
    arrow = re.compile(r"\s*→\s*")
    soup = _get_page()
    ready = False
    for row in soup.find_all(["div"], class_=["text-center"]):
        if "INTO → UNTO" in f"{row}":
            ready = True
            continue
        if ready and "row" in row.get("class"):
            ladder = arrow.split(row.text.lower())
            yield (ladder)


if __name__ == "__main__":
    pp(list(scrape_long_ladders()))
