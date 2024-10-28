#! /usr/bin/env python
from pathlib import Path

import typer


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


class LineCounter:

    def __init__(self, in_file: Path) -> None:
        with open(in_file) as fin:
            self.lines = list(map(str.rstrip, fin))
        self.blanks = sum(1 for line in self.lines if not line)
        self.comments = sum(1 for line in self.lines if line.startswith("#"))
        self.code = len(self.lines) - self.blanks - self.comments

    def counts(self) -> dict[str, int]:
        return {
            "blanks": self.blanks,
            "comments": self.comments,
            "code": self.code,
        }


def main(in_folder: Path) -> None:
    for file in get_source_files(in_folder):
        cnt = LineCounter(file)
        print(f"{len(cnt.lines):9,d}  lines in  {file}")


if __name__ == "__main__":
    typer.run(main)
