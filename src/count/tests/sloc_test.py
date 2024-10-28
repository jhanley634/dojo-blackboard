import unittest
from contextlib import redirect_stdout
from pathlib import Path

from count.sloc import LineCounter, get_source_files, main

_REPOS = Path("/tmp/repos")

SOURCES = [
    _REPOS / "llama.cpp",
    _REPOS / "docker-php-tutorial",
]

INITIAL_SOURCES = get_source_files(SOURCES[0])[:3]


class SlocTest(unittest.TestCase):

    def test_main(self) -> None:
        with redirect_stdout(None):
            main(SOURCES[0])

    def test_count_lines(self) -> None:
        for folder in SOURCES:
            assert folder.is_dir(), "Please run: $ make count"

        self.assertEqual(
            [
                "/tmp/repos/llama.cpp/tests/test-arg-parser.cpp",
                "/tmp/repos/llama.cpp/tests/test-llama-grammar.cpp",
                "/tmp/repos/llama.cpp/tests/test-rope.cpp",
            ],
            list(map(str, INITIAL_SOURCES)),
        )

        cnt = LineCounter(INITIAL_SOURCES[0])
        self.assertEqual(0, cnt.__dict__)
