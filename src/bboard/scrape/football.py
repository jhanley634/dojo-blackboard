#! /usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup

target_url = (
    "https://www.cnbc.com/2025/05/05/" "cnbcs-official-global-soccer-team-valuations-2025.html"
)
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0"


def main() -> None:
    resp = requests.get(target_url, headers={"User-Agent": ua})
    print(resp.status_code)
    html = resp.content
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())


if __name__ == "__main__":
    main()
