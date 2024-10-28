#! /usr/bin/env python
from pathlib import Path
from typing import NamedTuple

import typer


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


class Counts(NamedTuple):
    blanks: int
    comments: int
    code: int

    def __str__(self) -> str:
        return f"{self.blanks:5d} blanks   {self.comments:5d} comments   {self.code:5d} code"


class LineCounter:
    def __init__(self, in_file: Path) -> None:
        with open(in_file) as fin:
            self.lines = list(map(str.rstrip, fin))

    def counts(self) -> Counts:
        c = Counts(
            blanks=sum(1 for line in self.lines if not line),
            comments=sum(1 for line in self.lines if line.startswith("#")),
            code=0,
        )
        return c._replace(code=len(self.lines) - c.blanks - c.comments)


def main(in_folder: Path) -> None:
    for file in get_source_files(in_folder):
        cnt = LineCounter(file)
        print(f"{cnt.counts()}  lines in  {file}")


if __name__ == "__main__":
    typer.run(main)
