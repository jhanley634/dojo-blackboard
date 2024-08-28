#! /usr/bin/env python
from collections.abc import Generator

from src.bboard.util.credentials import read_api_keys
from src.bboard.util.fs import temp_dir


def _get_env_var_exports() -> Generator[str, None, None]:
    """Generates shell script "export" lines for setting API key environment variables."""
    for row in read_api_keys().itertuples():
        yield f"export {row.key_name}='{row.key_value}'"


def write_env_var_script(out_file: str = "secret_keys.sh") -> None:
    """Writes a shell script to set API key environment variables."""
    with open(temp_dir() / out_file, "w") as fout:
        fout.write("\n# usage:\n#    source /tmp/secret_keys.sh\n\n")
        for line in _get_env_var_exports():
            fout.write(f"{line}\n")


if __name__ == "__main__":
    write_env_var_script()
