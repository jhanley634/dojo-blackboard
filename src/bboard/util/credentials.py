"""
API key helpers.
"""

import csv
import tomllib
from os.path import devnull
from pathlib import Path
from shutil import copyfile
from typing import NoReturn

repo_top: Path = Path(__file__).resolve().parents[3]

secrets_dir: Path = (repo_top.parent / "dojo-secrets").resolve()


def get_api_key(name: str) -> str:
    assert is_enabled(name) or throw(ValueError(f"sorry, API key {name} is not enabled"))
    d = read_api_keys()
    return d[name]


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


def read_api_keys() -> dict[str, str]:
    in_file = secrets_dir / "api-keys.txt"
    in_file = file_exists(in_file) or Path(devnull)
    d: dict[str, str] = {}
    with open(in_file) as fin:
        reader = csv.DictReader(fin, delimiter="|")
        for row_ in reader:
            row = {k.strip(): str(v).strip() for k, v in row_.items()}
            if row["key_name"].startswith("--------"):
                continue
            d[row["key_name"]] = row["key_value"]
    return d
