#! /usr/bin/env python
"""
Counts source lines of code.
"""
import re
from collections import Counter
from collections.abc import Generator, Iterable
from enum import Enum, auto
from functools import partial
from pathlib import Path

import typer


class LineType(Enum):
    COMMENT = auto()  # indicates that a line starts with a comment, though code may follow
    CODE = auto()  # indicates that a line starts with code, though a comment may follow


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


_simple_comment_re = re.compile(r"^\s*//.*")
_slash_star_star_slash_re = re.compile(r"/\*.*\*/")
elide_comment_span = partial(_slash_star_star_slash_re.sub, " ")

COMMENT_MARKER = "// COMMENT "


class LineCounter:
    """Count blank, comment, and code lines in a C++ or PHP source file.

    We define "what cloc says" as the "correct" line counts.
    """

    def __init__(self, in_file: Path) -> None:
        with open(in_file) as fin:
            lines = list(map(str.rstrip, fin))

        self.blank = sum(1 for line in lines if not line)
        line_types = list(self._get_line_types(lines))
        self.comment = sum(bool(lt == LineType.COMMENT) for lt in line_types)
        self.code = sum(bool(lt == LineType.CODE) for lt in line_types)

        assert self.blank + self.comment + self.code == len(lines), len(lines)

    def __str__(self) -> str:
        return f"{self.blank:5d} blank   {self.comment:5d} comment   {self.code:5d} code"

    def _get_line_types(self, lines: list[str]) -> Generator[LineType, None, None]:
        for line in self.expand_comments(self._get_non_blank_lines(lines)):
            if _simple_comment_re.match(line):
                yield LineType.COMMENT
            else:
                yield LineType.CODE

    @staticmethod
    def expand_comments(lines: Iterable[str]) -> Generator[str, None, None]:
        """Prepends // marker to each commented line, accounting /* for multiline comments */."""
        initial_slash_star_re = re.compile(r"^\s*/\*")
        in_comment = False
        for line in lines:
            line = elide_comment_span(line)
            if initial_slash_star_re.match(line):
                line = COMMENT_MARKER + line
            if in_comment:
                line = COMMENT_MARKER + line
                i = line.find("*/")
                if i >= 0:
                    line = COMMENT_MARKER + line[i + 2 :]
                    in_comment = False
            if "/*" in line:
                assert "*/" not in line, line
                in_comment = True
            yield line

    @staticmethod
    def _get_non_blank_lines(lines: list[str]) -> Generator[str, None, None]:
        """This is `grep -v '^$'`.

        Recall that trailing whitespace has already been stripped.
        """
        for line in lines:
            if line:
                yield line


class BashLineCounter(LineCounter):
    """Count blank, comment, and code lines in a Bash script.

    Notice that Bash scripts have no notion of /* multiline comments */.
    """

    @staticmethod
    def expand_comments(lines: Iterable[str]) -> Generator[str, None, None]:
        """Prepends our standard COMMENT_MARKER to each commented line."""
        initial_hash_re = re.compile(r"^\s*#")
        for i, line in enumerate(lines):
            if i == 0 and line.startswith("#!"):
                line = "SHEBANG " + line
            if initial_hash_re.match(line):
                line = COMMENT_MARKER + line
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
