#! /usr/bin/env python
import re
from collections import Counter
from collections.abc import Generator
from enum import Enum, auto
from pathlib import Path

import typer


class LineType(Enum):
    COMMENT = auto()
    CODE = auto()


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


_strip_hash_re = re.compile(r"^\s*//.*")


class LineCounter:
    def __init__(self, in_file: Path) -> None:
        with open(in_file) as fin:
            lines = list(map(str.rstrip, fin))

        self.blank = sum(1 for line in lines if not line)
        line_types = list(self._get_line_types(lines))
        self.comment = sum(1 for line_type in line_types if line_type == LineType.COMMENT)
        self.code = sum(1 for line_type in line_types if line_type == LineType.CODE)

        assert self.blank + self.comment + self.code == len(lines), len(lines)

    def __str__(self) -> str:
        return f"{self.blank:5d} blank   {self.comment:5d} comment   {self.code:5d} code"

    def _get_line_types(self, lines: list[str]) -> Generator[LineType, None, None]:
        for line in self._get_non_blank_lines(lines):
            if _strip_hash_re.match(line):
                yield LineType.COMMENT
            else:
                yield LineType.CODE

    def _get_non_blank_lines(self, lines: list[str]) -> Generator[str, None, None]:
        """This is `grep -v '^$'`.

        Recall that trailing whitespace has already been stripped.
        """
        for line in lines:
            if line:
                yield line


def main(in_folder: Path) -> None:
    total = Counter({"blank": 0})
    for file in get_source_files(in_folder):
        cnt = LineCounter(file)
        print(f"{cnt}  lines in  {file}")
        total.update(cnt.__dict__)

    print("\ntotal:")
    for k, v in total.items():
        print(f"{v:5d} {k}   ", end="")
    print()


if __name__ == "__main__":
    typer.run(main)
