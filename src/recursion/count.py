#! /usr/bin/env python

# loosely based on https://stackoverflow.com/questions/79770935/why-does-python-limit-recursion-depth

import json
import sys
from pathlib import Path
from time import time

# from numba import jit
# from numba.core.registry import CPUDispatcher
# @jit  # type:ignore for def recursive_count()


def iterative_count(i: int, ceil: int) -> int:
    assert 0 == i, i  # Count up from zero, please.
    while i < ceil:
        i += 1
    return i


def recursive_count(i: int, ceil: int) -> int:
    if i < ceil:
        return recursive_count(i + 1, ceil)
    return int(i)


def main(n: int = 30_000_000) -> int:
    """Chooses large N, appropriate for current for current interpreter."""
    sys.setrecursionlimit(n + 10)
    if sys.version_info < (3, 11):
        n = 42_780  # max feasible value for interpreter 3.10.16
    if sys.version_info < (3, 10):  # noqa
        n = 72_287  # interpreters 3.8.20 & 3.9.23

    assert recursive_count(0, n) == n

    ver = sys.version.split()[0].ljust(9)
    print(end=f"{ver} {n:11,}")
    return n


TIMINGS = Path("/tmp/recursion/timings.jsonl")


if __name__ == "__main__":
    recursive_count(0, 990)  # warmup

    t0 = time()
    n = main()
    elapsed = time() - t0
    tput = f"{n / elapsed:,.1f}".rjust(13)
    print(f"  {elapsed:.6f} elapsed sec; {tput} count/sec")

    d = {
        "py": sys.version.split()[0].ljust(10),
        "n": n,
        "elapsed": float(f"{elapsed:.6f}"),
        "tput1m": float(tput.replace(",", "")) / 1e6,
    }
    with open(TIMINGS, "a") as fout:
        fout.write(f"{json.dumps(d)}\n")
