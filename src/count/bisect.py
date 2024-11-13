"""
Does a binary search to locate the first source code line
which produces a discrepancy between cloc and SlocTest.
"""

from functools import lru_cache
from pathlib import Path

from count.cloc import ClocCounts, get_cloc_triple
from count.sloc import LineCounter, get_counts

TEMP = Path("/tmp/bisect.d")


def find_delta(in_file: Path, *, paranoid: bool = False) -> int:
    TEMP.mkdir(exist_ok=True)
    with open(in_file) as fin:
        lines = fin.readlines()
    with open(TEMP / "bisect.log", "a") as fout:
        fout.write(f"{in_file=}\n")

    if paranoid:
        cloc_cnt = get_cloc_triple(in_file)
        assert cloc_cnt
        cnt = LineCounter(in_file)
        assert cloc_cnt != cnt, (cnt, in_file)
        assert cloc_cnt.blank == cnt.blank, (cnt, in_file)

    assert len(lines) > 0

    print(f"\n{in_file=}")

    return _bisect(len(lines), lines, in_file.suffix)


def _bisect(n: int, lines: list[str], suffix: str) -> int:
    """Locates the first source code line which produces a discrepancy
    between cloc and SlocTest.
    """
    assert suffix.startswith(".")

    if n <= 1 or n >= len(lines) - 2:
        return n

    mid = n // 2
    temp_file = TEMP / f"upto_{mid}{suffix}"
    if _counts_equal(mid, lines, temp_file) and not _counts_equal(mid + 1, lines, temp_file):
        return mid

    if _counts_equal(0, lines, temp_file):
        return _bisect(n - mid, lines[mid:], suffix)
    else:
        return _bisect(mid, lines[:mid], suffix)


@lru_cache
def _counts_equal(n: int, lines: list[str], temp_file: Path) -> bool:
    cloc_cnt, cnt = _get_both_counts(lines, temp_file)
    return cloc_cnt == cnt


def _get_both_counts(lines: list[str], temp_file: Path) -> tuple[ClocCounts, LineCounter]:
    with open(temp_file, "w") as fout:
        fout.writelines(lines)
    cloc_cnt = get_cloc_triple(temp_file)
    assert cloc_cnt
    return cloc_cnt, get_counts(temp_file)
