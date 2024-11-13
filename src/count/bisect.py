"""
Does a binary search to locate the first source code line
which produces a discrepancy between cloc and SlocTest.
"""

from pathlib import Path

from count.cloc import get_cloc_triple
from count.sloc import LineCounter

TEMP = Path("/tmp/bisect.d")


def delta_finder(in_file: Path) -> int:
    TEMP.mkdir(exist_ok=True)
    with open(in_file) as fin:
        lines = fin.readlines()
    with open(TEMP / "bisect.log", "a") as fout:
        fout.write(f"{in_file=}\n")

    cloc_cnt = get_cloc_triple(in_file)
    assert cloc_cnt
    cnt = LineCounter(in_file)
    assert cloc_cnt != cnt, (cnt, in_file)
    assert cloc_cnt.blank == cnt.blank, (cnt, in_file)

    assert len(lines) > 0
    return 0
