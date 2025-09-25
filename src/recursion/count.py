#! /usr/bin/env python

# from https://stackoverflow.com/questions/79770935/why-does-python-limit-recursion-depth

import sys


def iterative_count(i: int, ceil: int) -> int:
    assert 0 == i, i  # Count up from zero, please.
    while i < ceil:
        i += 1
    return i


def recursive_count(i: int, ceil: int) -> int:
    if i < ceil:
        return recursive_count(i + 1, ceil)
    return i


def main() -> None:
    big = 10_000_000  # 64_000 is safe on interpreter 3.8
    sys.setrecursionlimit(big + 10)

    n = 1_024
    if sys.version_info < (3, 11):
        n = big = 42_782  # max feasible value for interpreter 3.10.16
    if sys.version_info < (3, 10):
        n = big = 72_289  # interpreters 3.8.20 & 3.9.23

    while n <= big:
        print(f"{n:20,}")
        assert recursive_count(0, n) == iterative_count(0, n)
        n *= 2


if __name__ == "__main__":
    main()
