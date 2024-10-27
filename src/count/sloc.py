#! /usr/bin/env python
from pathlib import Path

import typer


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


def count_lines(in_file: Path) -> int:
    num_lines = 0

    with open(in_file) as fin:
        num_lines += len(fin.readlines())

    return num_lines


if __name__ == "__main__":
    typer.run(count_lines)
