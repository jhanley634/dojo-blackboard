#! /usr/bin/env python

from pathlib import Path

import pandas as pd

TEMP = Path("/tmp")


def get_pres(out_file: Path = TEMP / "pres.csv") -> None:
    """Reads several HTML tables from the given wiki page."""
    df = _get_df()
    print(df.to_markdown(index=False))
    with open(out_file, "w") as fout:
        fout.write(df.to_csv(index=False))


def _get_df() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"
    df = pd.read_html(url)[0]
    df = df.rename(
        columns={
            "No.[a]": "term",
            "Party[b][17].1": "party",
        }
    )
    for col in df.columns:
        # The en-dash in birth-death is tricky.
        if f"{col}".startswith("Name (birth"):
            df = df.rename(columns={col: "name"})
    df = df[["term", "party", "name"]]

    # Strip the (YYYY-YYYY) [NN] suffix, or (b. YYYY) for the still living.
    df["name"] = df["name"].str.replace(r" [(].*", "", regex=True)
    return df


if __name__ == "__main__":
    get_pres()
