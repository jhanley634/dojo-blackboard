#! /usr/bin/env python

# from https://stackoverflow.com/questions/79770935/why-does-python-limit-recursion-depth


def iterative_count(i: int, ceil: int) -> int:
    assert 0 == i, i  # Count up from zero, please.
    while i < ceil:
        i += 1
    return i


def recursive_count(i: int, ceil: int) -> int:
    if i < ceil:
        return recursive_count(i + 1, ceil)
    return i


if __name__ == "__main__":
    for n in range(600, 1_000, 100):
        print(n)
        assert recursive_count(0, n) == iterative_count(0, n)
