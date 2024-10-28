#! /usr/bin/env python
import re
from collections import Counter
from pathlib import Path
from pprint import pp

import typer


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


_strip_hash_re = re.compile(r"^\s*//.*")


class LineCounter:
    def __init__(self, in_file: Path) -> None:
        with open(in_file) as fin:
            lines = list(map(str.rstrip, fin))

        self.blanks = sum(1 for line in lines if not line)
        self.comments = sum(1 for line in lines if _strip_hash_re.search(line))
        self.code = sum(1 for line in lines if _strip_hash_re.sub("", line).strip())

        assert self.blanks + self.comments + self.code == len(lines), len(lines)

    def __str__(self) -> str:
        return f"{self.blanks:5d} blanks   {self.comments:5d} comments   {self.code:5d} code"


def main(in_folder: Path) -> None:
    summary = Counter({"blanks": 0})
    for file in get_source_files(in_folder):
        cnt = LineCounter(file)
        print(f"{cnt}  lines in  {file}")
        summary.update(cnt.__dict__)

    pp(summary)


if __name__ == "__main__":
    typer.run(main)
