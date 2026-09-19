#!/usr/bin/env python3
"""Refresh resumes/resume.pdf from the resumes repo, which owns the CV.

The CV is authored in ~/Personal/Resumes (github.com/rquinnmit/resumes) and
only *served* from here. A symlink would be the obvious way to say that, but
Pages builds from a checkout of this repo alone: a link pointing outside it
is dangling on the runner, and Jekyll skips symlinks regardless, so the CV
link would 404 in production. A copy plus this script is the honest version
of the same idea — the source of truth stays in one repo and this one holds a
build artifact that is cheap to regenerate.

Run from anywhere::

    python3 tools/sync-resume.py            # copy if the source differs
    python3 tools/sync-resume.py --check    # report only, exit 1 if stale

--check is what to run before publishing. It is deliberately not part of
tools/check.py: that script gates CI, and the source repo does not exist on
the runner.
"""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path.home() / "Personal" / "Resumes" / "2027" / "Ryan_Quinn___2027_Resume.pdf"
TARGET = ROOT / "resumes" / "resume.pdf"


def digest(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    check_only = "--check" in argv[1:]

    if not SOURCE.is_file():
        print(f"source missing: {SOURCE}")
        print("clone github.com/rquinnmit/resumes to ~/Personal/Resumes")
        return 1

    if TARGET.is_file() and digest(SOURCE) == digest(TARGET):
        print(f"ok: resumes/resume.pdf matches {SOURCE.name}")
        return 0

    if check_only:
        print(f"stale: resumes/resume.pdf differs from {SOURCE}")
        print("run: python3 tools/sync-resume.py")
        return 1

    shutil.copy2(SOURCE, TARGET)
    print(f"updated resumes/resume.pdf from {SOURCE}")
    print("commit it: the site serves this copy, not the source repo")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
