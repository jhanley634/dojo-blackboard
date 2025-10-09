from typing import TYPE_CHECKING

import pandas as pd
import requests

from bboard.util.requests import patch_requests_module

if TYPE_CHECKING:
    from collections.abc import Iterable

patch_requests_module()
CONNECTICUT_YANKEE = "https://www.gutenberg.org/cache/epub/86/pg86.txt"


# python -m spacy download en


def get_paragraphs(url: str = CONNECTICUT_YANKEE) -> Iterable[str]:
    """Uses spacy to produce the paragraphs of the given URL."""
    with requests.get(url) as response:  # type: ignore [attr-defined]
        response.raise_for_status()
        text = response.text.replace("\r\n", "\n")

    for paragraph in text.split("\n\n"):
        if paragraph.startswith("   "):
            continue
        yield paragraph.replace("\n", " ")


def main() -> None:
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp(paragraph)

    for paragraph in get_paragraphs():
        words = paragraph.split()
        df = pd.DataFrame(words, columns=["word"])
        df["len"] = df["word"].str.len()
        print(len(df), "\t", round(df["len"].mean(), 1), "\t", df["len"].std())


if __name__ == "__main__":
    main()
