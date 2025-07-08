#! /usr/bin/env python

from collections.abc import Generator
from pathlib import Path

from connections.conn_util import TOP

TALK_MD = TOP / "talks/2025-07-08-connections.md"


def _get_prompts(in_file: Path = TALK_MD) -> Generator[str]:
    titles = {
        "river crossing",
        "recent SC justices",
        "related word pairs",
    }
    with open(in_file) as fin:
        lines = fin.read().splitlines()
    i = 0
    while i < len(lines):
        if lines[i].removeprefix("# ") in titles:
            i, prompt = _grab_section(i, lines)
            yield prompt
        i += 1


def _grab_section(i: int, lines: list[str]) -> tuple[int, str]:
    """Grab lines of a prompt until we see a section marker.

    Reports on how far we went, and what we found.
    """
    prompt: list[str] = []
    line = lines[i].removeprefix("# ")
    while not line.startswith("#") and i < len(lines) - 1:
        if not line.startswith("\\"):
            prompt.append(line)
        i += 1
        line = lines[i]
    i -= 1  # just in case the "end of section" line is wanted for next section
    return i, "\n".join(prompt)


def store_prompts() -> None:
    for prompt in _get_prompts():
        print("\n\n===========\n\n")
        print(prompt)


if __name__ == "__main__":
    store_prompts()
