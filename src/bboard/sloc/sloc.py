#! /usr/bin/env python


from pathlib import Path

import typer


def count_sloc(in_file: Path) -> None:
    with open(in_file) as fin:
        lines = fin.readlines()
        print(len(lines))


if __name__ == "__main__":
    typer.run(count_sloc)
