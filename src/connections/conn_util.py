import pandas as pd


def validate(df: pd.DataFrame) -> None:
    for row in df.itertuples():
        category = f"{row.CATEGORY}"
        words = f"{row.WORDS}"
        assert category == category.upper(), row
        assert words == words.upper(), row
        commas = words.count(",")
        if commas != 3:
            print(commas, row)
