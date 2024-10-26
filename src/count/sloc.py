#! /usr/bin/env python
from pathlib import Path

import typer


def count_lines(in_files: list[Path]) -> None:
    for file in in_files:
        with open(file) as fin:
            print(f"{file} has {len(fin.readlines())} lines")


if __name__ == "__main__":
    typer.run(count_lines)
