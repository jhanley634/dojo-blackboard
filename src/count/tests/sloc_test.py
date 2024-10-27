import unittest
from pathlib import Path
from pprint import pp

from count.sloc import count_lines, get_source_files

_REPOS = Path("/tmp/repos")

SOURCES = [
    _REPOS / "llama.cpp",
    _REPOS / "docker-php-tutorial",
]


class SlocTest(unittest.TestCase):

    def test_count_lines(self) -> None:
        for folder in SOURCES:
            assert folder.is_dir(), "Please run: $ make count"

        self.assertEqual(
            [
                "/tmp/repos/llama.cpp/tests/test-arg-parser.cpp",
                "/tmp/repos/llama.cpp/tests/test-llama-grammar.cpp",
                "/tmp/repos/llama.cpp/tests/test-rope.cpp",
            ],
            list(map(str, get_source_files(SOURCES[0])))[:3],
        )

        d = {file: count_lines(file) for file in get_source_files(_REPOS)}
        pp(d)
        self.assertEqual(171, len(d))
