#! /usr/bin/env python
"""
Counts source lines of code.
"""
import re
from collections import Counter
from collections.abc import Iterable
from enum import Enum, auto
from functools import partial
from pathlib import Path

import typer


class LineType(Enum):
    BLANK = auto()  # indicates a line is blank
    COMMENT = auto()  # indicates a line starts with a comment, though code may follow
    CODE = auto()  # indicates a line starts with code, though a comment may follow


def get_source_files(folder: Path) -> list[Path]:
    files = list(folder.glob("**/*.cpp"))
    files += list(folder.glob("**/*.php"))
    return [file for file in files if file.is_file()]


_simple_comment_re = re.compile(r"^\s*//.*")
_slash_star_star_slash_re = re.compile(r"/\*.*\*/")
elide_slash_star_comment_span = partial(_slash_star_star_slash_re.sub, " ")

_long_xml_comment_re = re.compile(r"<!--.*-->")
elide_long_xml_comment_span = partial(_long_xml_comment_re.sub, " ")


COMMENT_MARKER = "// COMMENT "


class LineCounter:
    """Count blank, comment, and code lines in a C++ or PHP source file.

    We define "what cloc says" as the "correct" line counts.
    """

    def __init__(
        self,
        lines: Iterable[str] | Path,
        *,
        comment_pattern: str = r"^UNMATCHED_SENTINEL",
    ) -> None:
        self.suffix = ""
        if isinstance(lines, Path):
            self.suffix = lines.suffix
            lines = lines.read_text().splitlines()
        lines = list(map(str.rstrip, lines))

        self.comment_pattern = re.compile(comment_pattern)

        line_types = list(self._get_line_types(lines))
        self.blank = sum(bool(lt == LineType.BLANK) for lt in line_types)
        self.comment = sum(bool(lt == LineType.COMMENT) for lt in line_types)
        self.code = sum(bool(lt == LineType.CODE) for lt in line_types)
        delattr(self, "suffix")

    @property
    def counters(self) -> dict[str, int]:
        return {
            "blank": self.blank,
            "comment": self.comment,
            "code": self.code,
        }

    def __str__(self) -> str:
        return f"{self.blank:5d} blank   {self.comment:5d} comment   {self.code:5d} code"

    def _get_line_types(self, lines: list[str]) -> Iterable[LineType]:
        continuation = False  # tells whether the previous line ended with a backslash
        typ = LineType.COMMENT
        for line in self.expand_comments(self._do_shebang(lines)):
            if not continuation:
                if line.strip() == "":
                    typ = LineType.BLANK
                elif line.startswith(COMMENT_MARKER):
                    typ = LineType.COMMENT
                else:
                    typ = LineType.CODE
            yield typ
            continuation = line.endswith("\\")

    def expand_comments(self, lines: Iterable[str]) -> Iterable[str]:
        """Prepends // marker to each commented line, accounting /* for multiline comments */."""
        initial_slash_star_re = re.compile(r"^\s*/\*")
        in_comment = False
        for line in lines:
            line = elide_slash_star_comment_span(line)
            if initial_slash_star_re.match(line):
                line = COMMENT_MARKER + line
            if in_comment:
                line = COMMENT_MARKER + line
                i = line.find("*/")
                if i >= 0:
                    line = COMMENT_MARKER + line[i + 2 :]
                    in_comment = False
            if "/*" in line:
                in_comment = True
            if (
                self.comment_pattern
                and self.comment_pattern.match(line)
                and not line.startswith(COMMENT_MARKER)
            ):
                line = COMMENT_MARKER + line
            yield line

    @staticmethod
    def _do_shebang(lines: list[str]) -> Iterable[str]:
        """Prepend a marker to the shebang line."""
        if len(lines) > 0 and lines[0].startswith("#!"):
            lines[0] = f"SHEBANG {lines[0]}"

        yield from lines


class XmlLineCounter(LineCounter):

    def expand_comments(self, lines: Iterable[str]) -> Iterable[str]:
        """Prepends // marker to each commented line, accounting <!-- for multiline comments -->."""
        initial_long_comment_re = re.compile(r"^\s*<!--")
        in_comment = False
        for line in lines:
            if initial_long_comment_re.match(line):
                line = COMMENT_MARKER + line
            line = elide_long_xml_comment_span(line)

            if in_comment:
                line = COMMENT_MARKER + line
                i = line.find("-->")
                if i >= 0:
                    line = COMMENT_MARKER + line[i + 3 :]
                    in_comment = False
            if "<!--" in line:
                in_comment = True

            yield line


class BashLineCounter(LineCounter):
    """Count blank, comment, and code lines in a Bash script.

    Notice that Bash scripts have no notion of /* multiline comments */.
    """

    def expand_comments(self, lines: Iterable[str]) -> Iterable[str]:
        """Prepends our standard COMMENT_MARKER to each commented line."""
        for line in lines:
            if self.comment_pattern.match(line):
                line = COMMENT_MARKER + line
            yield line


class PythonLineCounter(LineCounter):
    '''Count blank, comment, and code lines in a Python script.

    The cloc command views """multiline string constants""" similar
    to the /* multiline comments */ of other languages, independent of whether
    they're being used in a function docstring.
    '''

    def expand_comments(self, lines: Iterable[str]) -> Iterable[str]:
        """Prepends our standard COMMENT_MARKER to each commented line."""
        initial_triple_quote_re = re.compile(r'^\s*"""')
        initial_hash_re = re.compile(r"^\s*#")
        in_comment = False
        for line in lines:
            line = line.replace("'''", '"""')  # Pretend that all authors follow PEP 8's advice.
            if initial_triple_quote_re.match(line) or initial_hash_re.match(line):
                line = COMMENT_MARKER + line
            if in_comment:
                line = COMMENT_MARKER + line
                i = line.find('"""')
                if i >= 0:
                    line = COMMENT_MARKER + line[i + 2 :]
                    in_comment = False
            if '"""' in line:
                # Hope the original author followed convention, as the SLOC code didn't ensure this.
                in_comment = True
            yield line


HASH_MEANS_COMMENT_LANGUAGES = frozenset(
    {
        ".Dockerfile",
        ".cmake",
        ".in",
        ".mk",
        ".pro",
        ".properties",
        ".sh",
        ".toml",
        ".yaml",
        ".yml",
    }
)
XML_LANGUAGES = frozenset(
    {
        ".htm",
        ".html",
        ".svg",
        ".xml",
    }
)


def get_counts(file: Path) -> LineCounter:
    line_counter: type[LineCounter] = LineCounter
    kwargs = {"comment_pattern": r"^UNMATCHED_SENTINEL$"}
    if file.suffix in XML_LANGUAGES:
        line_counter = XmlLineCounter
    if file.suffix in HASH_MEANS_COMMENT_LANGUAGES:
        line_counter, kwargs = BashLineCounter, {"comment_pattern": r"^\s*#"}
    match file.suffix:
        case ".bat":
            line_counter, kwargs = BashLineCounter, {"comment_pattern": r"^rem |^::"}
        case ".cu":
            line_counter, kwargs = BashLineCounter, {"comment_pattern": r"^\s*//"}
        case ".ini":
            line_counter, kwargs = BashLineCounter, {"comment_pattern": r"^;"}
        case ".json":
            line_counter, kwargs = BashLineCounter, {"comment_pattern": r"^JSON_LACKS_COMMENTS"}
        case ".php":
            line_counter, kwargs = LineCounter, {"comment_pattern": r"^\s*//"}
        case ".py":
            line_counter = PythonLineCounter

    return line_counter(file, **kwargs)


def main(in_folder: Path) -> None:
    total = Counter({"blank": 0})
    for file in get_source_files(in_folder):
        cnt = LineCounter(file)
        print(f"{cnt}  lines in  {file}")
        total |= cnt.counters

    print("\ntotal:")
    for k, v in total.items():
        print(f"{v:5d} {k}   ", end="")
    print()


if __name__ == "__main__":
    typer.run(main)
