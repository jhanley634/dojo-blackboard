"""
API key helpers.
"""

import tomllib
from os.path import devnull
from pathlib import Path
from shutil import copyfile
from typing import NoReturn

import pandas as pd

repo_top = Path(__file__).resolve().parents[3]

secrets_dir = (repo_top.parent / "dojo-secrets").resolve()


def get_api_key(name: str) -> str:
    assert is_enabled(name) or throw(ValueError(f"sorry, API key {name} is not enabled"))
    df = read_api_keys()
    df = df[df["key_name"] == name]
    assert 1 == len(df), (name, df)
    return str(df.key_value[1])


def throw(e: Exception) -> NoReturn:
    """Turns `raise`, which is a statement, into an expression."""
    raise e


def file_exists(file: Path) -> Path | None:
    if file.exists():
        return file
    return None


def is_enabled(key_name: str) -> bool:
    """Predicate, returns True if we should attempt API calls using the given key.

    Note that a key missing from the config file will default to False, "disabled".
    """
    key_config_toml = repo_top / "key-config.toml"
    assert key_config_toml.exists() or copyfile(f"{key_config_toml}.example", key_config_toml)
    with open(key_config_toml, "rb") as fin:
        d = tomllib.load(fin)
        enabled = bool(d["enabled"].get(key_name))
        return enabled and secrets_dir.exists()


def read_api_keys() -> pd.DataFrame:
    in_file = secrets_dir / "api-keys.txt"
    in_file = file_exists(in_file) or Path(devnull)
    sep = r"\s*\|\s*"
    df: pd.DataFrame = pd.read_csv(in_file, sep=sep, engine="python", skiprows=[1])
    c = df.columns
    df = df.drop(columns=[c[0], c[-1]])
    return df
