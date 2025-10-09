#! /usr/bin/env python

import json
from typing import TYPE_CHECKING, Any

import polars as pl

from src.recursion.count import TIMINGS

if TYPE_CHECKING:
    from pathlib import Path


def _read_lines(jsonl: Path) -> list[dict[str, Any]]:
    with open(jsonl) as fin:
        return [json.loads(line) for line in fin]


if __name__ == "__main__":
    df = pl.DataFrame(_read_lines(TIMINGS))
    print(df)
