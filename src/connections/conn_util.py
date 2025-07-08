from collections.abc import Generator
from pathlib import Path

import pandas as pd

TOP = Path().absolute()
CONNECTIONS_EXAMPLES = TOP / "src/connections/connections.txt"


def get_examples(in_file: Path = CONNECTIONS_EXAMPLES) -> Generator[dict[str, list[str] | str]]:
    with open(in_file) as fin:
        line = next(fin)
        assert "-*- org -*-\n" == line, line
        hdr: list[str] = []

        for line in fin:
            line = line.removeprefix("| ").removesuffix("|\n").strip()
            if line.startswith("|----") or not line.removesuffix("|"):
                continue

            cols = line.split("| ")
            assert 2 == len(cols)

            cols[0] = cols[0].rstrip()
            if not hdr:  # initial line
                hdr = list(map(str.lower, cols))
                continue
            cat = cols[0]
            words = cols[1].split(", ")
            assert 4 == len(words), words

            yield dict(zip(hdr, [cat, words], strict=True))


def validate(df: pd.DataFrame) -> None:
    for row in df.itertuples():
        category = f"{row.category}"
        words = f"{row.words}"
        assert category == category.upper(), row
        assert words == words.upper(), row
        commas = words.count(",")
        if commas != 3:
            print(commas, row)
