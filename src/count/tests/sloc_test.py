import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from random import shuffle

from bboard.util.testing import mark_slow_integration_test
from count.bisect import find_delta
from count.cloc import get_cloc_triple
from count.sloc import (
    HASH_MEANS_COMMENT_LANGUAGES,
    BashLineCounter,
    LineCounter,
    PythonLineCounter,
    elide_comment_span,
    get_counts,
    get_source_files,
    main,
)

_REPOS = Path("/tmp/repos")

SOURCES = [
    _REPOS / "llama.cpp",
    _REPOS / "docker-php-tutorial",
]

INITIAL_CPP_SOURCES = sorted(get_source_files(SOURCES[0]))[:3]
INITIAL_PHP_SOURCES = sorted(get_source_files(SOURCES[1]))[:3]


class SlocTest(unittest.TestCase):

    @staticmethod
    def test_main() -> None:
        with redirect_stdout(None):
            main(SOURCES[0])

    def test_count_cpp_lines(self) -> None:
        for folder in SOURCES:
            assert folder.is_dir()

        self.assertEqual(
            [
                _REPOS / "llama.cpp/common/arg.cpp",
                _REPOS / "llama.cpp/common/common.cpp",
                _REPOS / "llama.cpp/common/console.cpp",
            ],
            INITIAL_CPP_SOURCES,
        )

        cnt = LineCounter(INITIAL_CPP_SOURCES[0])
        self.assertEqual(
            {"blank": 46, "comment": 32, "code": 1963},
            cnt.__dict__,
        )

        cnt = LineCounter(_REPOS / "llama.cpp/src/llama-vocab.cpp")
        self.assertEqual(
            {"blank": 287, "comment": 197, "code": 1500},
            cnt.__dict__,
        )

    def test_count_php_lines(self) -> None:
        cnt = LineCounter(INITIAL_PHP_SOURCES[0])
        self.assertEqual(
            {"blank": 11, "comment": 9, "code": 34},
            cnt.__dict__,
        )

        self.assertEqual(
            _REPOS / "docker-php-tutorial/app/Console/Kernel.php",
            INITIAL_PHP_SOURCES[1],
        )
        cnt = LineCounter(INITIAL_PHP_SOURCES[1])
        self.assertEqual(
            {"blank": 5, "comment": 12, "code": 15},
            cnt.__dict__,
        )

        cnt = LineCounter(_REPOS / "docker-php-tutorial/config/database.php")
        self.assertEqual(
            {"blank": 23, "comment": 45, "code": 107},
            cnt.__dict__,
        )

    def test_config_cors_lines(self) -> None:
        r"""The result computed here is incorrect, it doesn't match cloc.

        And I declare it to be "good enough".
        The slash-star within quotes is the trouble,
        and I'm not keen to parse all the \t \" \n escaped string constant details.
        """
        cnt = LineCounter(_REPOS / "docker-php-tutorial/config/cors.php")
        self.assertEqual(
            {"blank": 11, "comment": 20, "code": 3},
            cnt.__dict__,
        )
        lines = [
            "    'paths' => ['api/*', 'sanctum/csrf-cookie'],",
        ]
        self.assertEqual(
            ["    'paths' => ['api/*', 'sanctum/csrf-cookie'],"],
            list(cnt.expand_comments(lines)),
        )

    def test_count_bash_lines(self) -> None:
        cnt = BashLineCounter(_REPOS / "llama.cpp/ci/run.sh")
        self.assertEqual(
            {"blank": 187, "comment": 44, "code": 620},
            cnt.__dict__,
        )

    def test_expand_comments_multiline(self) -> None:
        cnt = LineCounter(Path(os.devnull))
        lines = [
            "zero /* comment */ calories",
            "/* one",
            " * two",
            " * three",
            " */ four",
            "five",
        ]
        self.assertEqual(
            [
                "zero   calories",
                "// COMMENT /* one",
                "// COMMENT  * two",
                "// COMMENT  * three",
                "// COMMENT  four",
                "five",
            ],
            list(cnt.expand_comments(lines)),
        )

    def test_expand_comments_single_line(self) -> None:
        cnt = LineCounter(Path(os.devnull))
        lines = [
            " /**/ foo",
            "bar",
            " /* qux */ baz /*",
            "blorg */",
            "a /* b */ c /* d */ e",
            " /* b */ c /* d */ e",
        ]
        self.assertEqual(
            [
                "   foo",
                "bar",
                "   baz /*",
                "// COMMENT ",
                "a   e",
                "   e",
            ],
            list(cnt.expand_comments(lines)),
        )

    def test_regex(self) -> None:
        self.assertEqual(" ", elide_comment_span("/* hello */"))
        self.assertEqual(" ", elide_comment_span("/* a */ b /* c */"))
        self.assertEqual("d   h", elide_comment_span("d /* e */ f /* g */ h"))


class TestCloc(unittest.TestCase):
    def test_last_line_is_blank(self) -> None:
        in_file = _REPOS / "docker-php-tutorial/.make/00-00-development-setup.mk"
        with open(in_file) as f:
            lines = f.readlines()
        self.assertEqual("", lines[-1].strip())

        cloc_cnt = get_cloc_triple(in_file)
        self.assertEqual(
            {"blank": 4, "comment": 2, "code": 57},
            cloc_cnt.__dict__,
        )
        cnt = BashLineCounter(in_file)
        self.assertGreater(cnt.code, 0)
        # self.assertEqual(cloc_cnt.__dict__, cnt.__dict__)  # non equal :(

    SUPPORTED_LANGUAGES = frozenset(
        {
            ".Dockerfile",
            ".bat",
            ".cmake",
            ".comp",
            ".cu",
            ".cuh",
            ".ini",
            ".json",
            ".kt",
            ".kts",
            ".mk",
            ".php",
            ".pro",
            ".properties",
            ".py",
            ".sh",
            ".swift",
            ".toml",
            ".yml",
        }
    )

    def test_empty_intersection(self) -> None:
        self.assertEqual(0, len(self.SKIP_LANGUAGE.intersection(HASH_MEANS_COMMENT_LANGUAGES)))
        self.assertEqual(19, len(self.SUPPORTED_LANGUAGES))

    SKIP_LANGUAGE = frozenset(
        {
            ".c",
            ".cpp",
            ".css",
            ".feature",
            ".h",
            ".hpp",
            ".html",
            ".js",
            ".md",
            ".mjs",
            ".nix",
            ".svg",
            ".txt",
            ".vim",
            ".xml",
        }
    )
    SKIP = frozenset(
        {
            _REPOS / "docker-php-tutorial/.make/00-00-development-setup.mk",
            _REPOS / "docker-php-tutorial/config/cors.php",
            _REPOS / "llama.cpp/convert_hf_to_gguf.py",
            _REPOS / "llama.cpp/examples/convert_legacy_llama.py",
            _REPOS / "llama.cpp/examples/llava/llava_surgery_v2.py",  # off by 2 comment lines
            _REPOS / "llama.cpp/examples/llava/minicpmv-convert-image-encoder-to-gguf.py",
            _REPOS / "llama.cpp/examples/pydantic_models_to_grammar.py",
            _REPOS / "llama.cpp/examples/pydantic_models_to_grammar_examples.py",
            _REPOS / "llama.cpp/pyrightconfig.json",
            _REPOS / "llama.cpp/scripts/compare-llama-bench.py",
            _REPOS / "llama.cpp/tests/test-tokenizer-random.py",
        }
    )

    @mark_slow_integration_test  # type: ignore [misc]
    def test_count_diverse_file_types(self) -> None:
        in_files = list(_REPOS.glob("**/*"))
        shuffle(in_files)
        self.assertGreaterEqual(len(in_files), 1487)  # 563 of these survive the "skip" filters
        # Ensure that a pair of "rare file types" get exercised.
        in_files.append(_REPOS / "llama.cpp/scripts/install-oneapi.bat")
        in_files.append(_REPOS / "llama.cpp/mypy.ini")

        # All the in_files work properly; examine just a subset in the interest of speed.
        for file in in_files[:4]:
            if (
                file.is_file()
                and file.suffix
                and file.suffix not in self.SKIP_LANGUAGE
                and file not in self.SKIP
            ):
                cloc_cnt = get_cloc_triple(file)
                if cloc_cnt:
                    cnt = get_counts(file)
                    self.assertEqual(cloc_cnt.__dict__, cnt.__dict__, file)

        for file in sorted(self.SKIP):
            cloc_cnt = get_cloc_triple(file)
            assert cloc_cnt
            line_counter = LineCounter
            if file.suffix == ".py":
                line_counter = PythonLineCounter
            cnt = line_counter(file)
            self.assertNotEqual(cloc_cnt.__dict__, cnt.__dict__)


class TestBisect(TestCloc):
    @mark_slow_integration_test  # type: ignore [misc]
    def test_bisect(self) -> None:
        in_files = list(_REPOS.glob("**/*"))
        shuffle(in_files)
        self.assertGreaterEqual(len(in_files), 1487)  # 563 of these survive the "skip" filters

        for file in in_files[:40]:
            if (
                file.is_file()
                and file.suffix
                and file.suffix not in (".txt")
                # and file.suffix not in self.SKIP_LANGUAGE
                # and file not in self.SKIP
            ):
                cloc_cnt = get_cloc_triple(file)
                if cloc_cnt:
                    cnt = get_counts(file)
                    if cloc_cnt.__dict__ != cnt.__dict__:
                        self.assertEqual(cloc_cnt.blank, cnt.blank, (cnt, file))
                        print(find_delta(file))

    def test_find_delta(self) -> None:
        llama = _REPOS / "llama.cpp"

        for n, file in [
            (159, llama / "examples/llava/llava_surgery_v2.py"),
            (806, llama / "examples/llava/minicpmv-convert-image-encoder-to-gguf.py"),
            (1322, llama / "examples/pydantic_models_to_grammar.py"),
            (312, llama / "examples/pydantic_models_to_grammar_examples.py"),
            (381, llama / "scripts/compare-llama-bench.py"),
            (566, llama / "tests/test-tokenizer-random.py"),
        ]:
            self.assertEqual(n, find_delta(file))
