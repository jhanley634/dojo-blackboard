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
        fout.write(f"{in_file}\n")

    if paranoid:
        cloc_cnt = get_cloc_triple(in_file)
        assert cloc_cnt
        cnt = LineCounter(in_file)
        assert cloc_cnt != cnt, (cnt, in_file)
        assert cloc_cnt.blank == cnt.blank, (cnt, in_file)

    assert len(lines) > 0

    print(f"\n{in_file=}")

    bisector = DiscrepancyFinder(lines, in_file.suffix)
    return bisector.bisect(len(lines))


class DiscrepancyFinder:

    def __init__(self, lines: list[str], suffix: str) -> None:
        assert suffix.startswith(".")

        self.lines = lines
        self.suffix = suffix

    def bisect(self, n: int) -> int:
        """Locates the first source code line which produces a discrepancy
        between cloc and SlocTest.
        """
        print(n)

        lines = self.lines
        if n <= 1 or n >= len(lines) - 2:
            return n

        assert not self._counts_equal(len(lines) - 1), n

        mid = n // 2
        eq_p0 = self._counts_equal(mid + 0)
        eq_p1 = self._counts_equal(mid + 1)
        if eq_p0 and not eq_p1:
            return mid + 1
        if eq_p0:
            return self.bisect(n + mid)
        return self.bisect(mid)

    @lru_cache
    def _counts_equal(self, n: int) -> bool:
        cloc_cnt, cnt = self._get_both_counts(n)
        return dict(cloc_cnt.__dict__) == dict(cnt.__dict__)

    def _get_both_counts(self, n: int) -> tuple[ClocCounts, LineCounter]:
        temp_file = TEMP / f"upto_{n}{self.suffix}"
        print(n, "\t", temp_file)
        with open(temp_file, "w") as fout:
            fout.writelines(self.lines[:n])
        cloc_cnt = get_cloc_triple(temp_file)
        assert cloc_cnt
        return cloc_cnt, get_counts(temp_file)
