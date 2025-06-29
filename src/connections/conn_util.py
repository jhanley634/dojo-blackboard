from pathlib import Path

import pandas as pd

TOP = Path().absolute()
IN_FILE = TOP / "src/connections/connections.txt"


def get_examples(in_file: Path = IN_FILE) -> pd.DataFrame:
    lines = in_file.read_text()
    print(lines)
    return pd.DataFrame()


def validate(df: pd.DataFrame) -> None:
    for row in df.itertuples():
        category = f"{row.CATEGORY}"
        words = f"{row.WORDS}"
        assert category == category.upper(), row
        assert words == words.upper(), row
        commas = words.count(",")
        if commas != 3:
            print(commas, row)
