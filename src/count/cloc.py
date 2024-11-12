"""
Interface code for calling /usr/local/bin/cloc.
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClocCounts:
    """Models the output of the cloc command."""

    blank: int
    comment: int
    code: int


_boilerplate_re = re.compile(r"^Language\s+files\s+blank\s+comment\s+code$")
_counts_re = re.compile(r"^[\w+-]+\s+1\s+(\d+)\s+(\d+)\s+(\d+)$")


def get_cloc_triple(in_file: Path) -> ClocCounts | None:
    """Calls the cloc command and parses the output."""

    result = subprocess.check_output(["/usr/local/bin/cloc", in_file]).decode()
    lines = result.split("\n")

    assert lines[-1] == "", lines[-1]
    if len(lines) == 1:
        return None
    assert 7 == len(lines), (len(lines), in_file)
    assert lines[-2].startswith("--------"), lines[-1]
    assert lines[-4].startswith("--------")
    assert _boilerplate_re.search(lines[-5]), lines[-5]

    m = _counts_re.search(lines[-3])
    assert m, f">{lines[-3]}<"

    return ClocCounts(*map(int, m.groups()))
