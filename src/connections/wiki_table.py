#! /usr/bin/env python

from pathlib import Path

import pandas as pd

TEMP = Path("/tmp")


def get_pres(out_file: Path = TEMP / "pres.csv") -> None:
    """Reads several HTML tables from the given wiki page."""
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    df = pd.read_html(url)[0]
    # print(df.to_markdown())
    print(df.to_csv(index=False))



if __name__ == "__main__":
    get_pres()
