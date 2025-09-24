#! /usr/bin/env python

import re
from pathlib import Path
from subprocess import check_output

REQ = Path("requirements.txt")


def read_old(req: Path = REQ) -> dict[str, str]:
    pat = re.compile(r"^([\w[\]-]+) *>?=+ *(.*)")
    d = {"": ""}

    pkg_versions = check_output(
        ["uv", "pip", "list", "--format=freeze"],
        text=True,
    )
    for line in pkg_versions.splitlines():
        m = pat.match(line)
        assert m, line
        pkg, version = m.groups()
        d[pkg] = version

    ret = {"fastapi[standard]": "0.117.1"}
    with open(req) as fin:
        for line in fin:
            m = pat.search(line)
            assert m, line
            pkg = m[1]
            if pkg not in ret:
                ver = d[pkg]
                ret[pkg] = ver

    return ret


def write_new(d: dict[str, str], req: Path = REQ) -> None:
    with open(req, "w") as fout:
        for pkg in sorted(d):
            ver = d[pkg]
            fout.write(f"{pkg} >= {ver}\n")


if __name__ == "__main__":
    write_new(read_old())
