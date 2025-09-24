#! /usr/bin/env python

import re
from pathlib import Path
from pprint import pp
from subprocess import check_output

REQ = "requirements.txt"


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

    pp(d)
    skip = (
        "fastapi[standard]",
        "lxml_html_clean",
    )
    ret = {
        "basemap": "1.4.1",
        "fastapi[standard]": "0.115.4",
        "lxml_html_clean": "0.4.1",
    }
    with open(req) as fin:
        for line in fin:
            m = pat.search(line)
            assert m, line
            pkg = m[1]
            if pkg not in skip:
                ver = d[pkg]
                ret[pkg] = ver
                print(pkg, "\t", ver)

    return ret


def write_new(d: dict[str, str], req: Path = REQ) -> None:
    with open(req, "w") as fout:
        for pkg in sorted(d)[1:]:
            ver = d[pkg]
            fout.write(f"{pkg} >= {ver}\n")


if __name__ == "__main__":
    d = read_old()
    pp(d)
    write_new(d)
