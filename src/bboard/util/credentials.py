"""
API key helpers.
"""

from pathlib import Path
from typing import NoReturn

import pandas as pd

repo_top = Path(__file__).resolve().parents[3]

secrets_dir = (repo_top.parent / "dojo-secrets").resolve()


def get_api_key(name: str) -> str:
    df = read_api_keys()
    df = df[df["key_name"] == name]
    assert 1 == len(df), (name, df)
    return str(df.key_value[1])  # pyright: ignore (reportUnknownVariableType)


# mypy: disable-error-code="unused-ignore"


def read_api_keys() -> pd.DataFrame:
    diagnostic = f"Please clone a repo at {secrets_dir}"
    secrets_dir.is_dir() or throw(FileNotFoundError(diagnostic))  # type: ignore [reportUnusedExpression]
    in_file = secrets_dir / "api-keys.txt"
    sep = r"\s*\|\s*"
    df: pd.DataFrame = pd.read_csv(in_file, sep=sep, engine="python", skiprows=[1])
    c = df.columns
    df = df.drop(columns=[c[0], c[-1]])
    return df


def throw(e: Exception) -> NoReturn:
    """Turns `raise`, which is a statement, into an expression."""
    raise e
