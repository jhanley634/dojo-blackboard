#! /usr/bin/env python

from typing import TYPE_CHECKING

from bboard.util.credentials import read_api_keys
from bboard.util.fs import temp_dir

if TYPE_CHECKING:
    from collections.abc import Generator


def _get_env_var_exports() -> Generator[str]:
    """Generates shell script "export" lines for setting API key environment variables."""
    for name, value in read_api_keys().items():
        yield f"export {name}='{value}'"


def write_env_var_script(out_file: str = "secret_keys.sh") -> None:
    """Writes a shell script to set API key environment variables."""
    out_path = temp_dir() / out_file
    with open(out_path, "w") as fout:
        fout.write(f"\n# usage:\n#    source {out_path}\n\n")
        fout.writelines(_get_env_var_exports())

    out_path.chmod(0o600)  # only owner may read the secrets


if __name__ == "__main__":
    write_env_var_script()
