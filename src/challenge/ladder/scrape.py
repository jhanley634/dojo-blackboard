from pathlib import Path

from bs4 import BeautifulSoup
from requests_cache import CachedSession


def _get_page() -> BeautifulSoup:
    tmp = Path("/tmp")
    session = CachedSession(
        tmp / "word_list_cache",
        backend="filesystem",
    )
    url = "http://datagenetics.com/blog/april32019/"
    resp = session.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def scrape() -> None:
    soup = _get_page()
    ready = False
    for row in soup.find_all("div", class_=["text-center"]):
        if "INTO → UNTO" in f"{row}":
            ready = True
            continue
        if ready and "row" in row.get("class"):
            print()
            print(row.text)


if __name__ == "__main__":
    scrape()
