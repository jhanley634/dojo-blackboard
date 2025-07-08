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
        for line in fin:
            line = line.removeprefix("# ").rstrip()
            if line in titles:
                prompt: list[str] = []
                while not line.startswith("#"):
                    if not line.startswith("\\"):
                        prompt.append(line)
                    line = next(fin).rstrip()
                yield "\n".join(prompt)


def store_prompts() -> None:
    for prompt in _get_prompts():
        print("\n\n===========\n\n")
        print(prompt)


if __name__ == "__main__":
    store_prompts()
