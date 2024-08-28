"""
API key helpers.
"""

from pathlib import Path
from typing import NoReturn

import pandas as pd

top_dir = Path(__file__).resolve().parents[3]
secrets_dir = (top_dir.parent / "dojo-secrets").resolve()


def read_api_keys() -> pd.DataFrame:
    diagnostic = f"Please clone a repo at {secrets_dir}"
    secrets_dir.is_dir() or throw(FileNotFoundError(diagnostic))
    in_file = secrets_dir / "api-keys.txt"
    sep = r"\s*\|\s*"
    df = pd.read_csv(in_file, sep=sep, engine="python", skiprows=[1])
    c = df.columns
    df = df.drop(columns=[c[0], c[-1]])
    return df


def throw(e: Exception) -> NoReturn:
    """Turns `raise`, which is a statement, into an expression."""
    raise e
