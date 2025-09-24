#! /usr/bin/env python

# from https://stackoverflow.com/questions/79770935/why-does-python-limit-recursion-depth


def count(i, ceil):
    if i < ceil:
        return count(i + 1, ceil)
    return i
