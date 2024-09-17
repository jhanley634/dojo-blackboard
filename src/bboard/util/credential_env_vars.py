#! /usr/bin/env python
from collections.abc import Generator

from bboard.util.credentials import read_api_keys
from bboard.util.fs import temp_dir


def _get_env_var_exports() -> Generator[str, None, None]:
    """Generates shell script "export" lines for setting API key environment variables."""
    for row in read_api_keys().itertuples():
        yield f"export {row.key_name}='{row.key_value}'"


def write_env_var_script(out_file: str = "secret_keys.sh") -> None:
    """Writes a shell script to set API key environment variables."""
    out_path = temp_dir() / out_file
    with open(out_path, "w") as fout:
        fout.write(f"\n# usage:\n#    source {out_path}\n\n")
        for line in _get_env_var_exports():
            fout.write(f"{line}\n")

    out_path.chmod(0o600)  # only owner may read the secrets


if __name__ == "__main__":
    write_env_var_script()
