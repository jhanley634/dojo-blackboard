#! /usr/bin/env python

from collections.abc import Generator
from datetime import timedelta
from io import StringIO

import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup, NavigableString, Tag

_one_day = timedelta(days=1).total_seconds()
requests_cache.install_cache("/tmp/scraping_cache", expire_after=_one_day)


target_url = (
    "https://www.cnbc.com/2025/05/05/cnbcs-official-global-soccer-team-valuations-2025.html"
)
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0"


def _get_col_headers(table: Tag | NavigableString | None) -> Generator[str]:
    assert isinstance(table, Tag)
    trs = table.find("tr")
    assert trs
    for header in trs:
        assert isinstance(header, Tag)
        yield str(header.get_text(strip=True))


def main() -> None:
    resp = requests.get(target_url, headers={"User-Agent": ua})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    dfs = pd.read_html(StringIO(resp.text))
    assert 1 == len(dfs)
    df = dfs[0].iloc[1:]  # suppress initial "data" row, which is actually "headers"
    df.columns = pd.Index(_get_col_headers(soup.find("table")))
    df = df.rename(columns={"Debt as % of value": "debt_pct"})
    df["debt_pct"] = pd.to_numeric(df.debt_pct.str.rstrip("%").astype(str), errors="coerce")
    df["RANK"] = pd.to_numeric(df.RANK)
    # There is room for improvement on the "$nnnM" or "$nnnB" Value, Revenue, EBITDA columns.
    # That last one is especially simple, since figures are always in millions, e.g. "-$29M".

    print(df.to_markdown(index=False))


if __name__ == "__main__":
    main()
