#! /usr/bin/env python
from pathlib import Path

import typer


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


def count_lines(in_file: Path) -> int:
    with open(in_file) as fin:
        return len(fin.readlines())


def main(in_folder: Path) -> None:
    for file in get_source_files(in_folder):
        print(f"{count_lines(file):9,d}  lines in  {file}")


if __name__ == "__main__":
    typer.run(main)
