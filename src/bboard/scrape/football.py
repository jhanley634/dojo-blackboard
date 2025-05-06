#! /usr/bin/env python

from datetime import timedelta
from io import StringIO

import pandas as pd
import requests
import requests_cache

_one_day = timedelta(days=1).total_seconds()
requests_cache.install_cache("/tmp/scraping_cache", expire_after=_one_day)


target_url = (
    "https://www.cnbc.com/2025/05/05/cnbcs-official-global-soccer-team-valuations-2025.html"
)
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0"


def main() -> None:
    resp = requests.get(target_url, headers={"User-Agent": ua})
    resp.raise_for_status()

    dfs = pd.read_html(StringIO(resp.text))
    assert 1 == len(dfs)
    df = dfs[0]
    print(df.to_markdown(index=False))

    # print(BeautifulSoup(html, "html.parser").prettify())


if __name__ == "__main__":
    main()
