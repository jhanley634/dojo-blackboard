#! /usr/bin/env python

import re
from typing import TYPE_CHECKING

from connections.conn_util import TOP

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

TALKS = TOP / "talks"
TALK_MD = TALKS / "2025-07-08-connections.md"


def _get_prompts(in_file: Path = TALK_MD) -> Generator[str]:
    titles = {
        "river crossing",
        "SC justices",
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


RESULT = TALKS / "asset/result"


def store_prompts(result_dir: Path = RESULT) -> None:
    result_dir.mkdir(exist_ok=True)
    title_re = re.compile(r"^[\w ]+")
    no_punct = str.maketrans("", "", r'''"'"''')

    for prompt in _get_prompts():
        m = title_re.search(prompt)
        assert m
        name = m[0].replace(" ", "-").translate(no_punct)

        with open(result_dir / f"prompt-{name}.md", "w") as fout:
            fout.write(prompt)


if __name__ == "__main__":
    store_prompts()
