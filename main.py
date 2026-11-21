#!/usr/bin/env python3
"""Entrypoint for news-image-20261121.

Copies the pre-rendered front page (entry.png, built at authoring time by
draw.py with PIL) into the output directory as entry.png. The copy is
byte-for-byte, so both graded runs produce identical output.

Standard library only; no network access. The output directory is a mounted
volume: it is created if missing and never removed.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) == 0:
        raise SystemExit("entry.png copied but empty")
    if _sha256(src) != _sha256(dst):
        raise SystemExit("entry.png copy failed integrity check")


if __name__ == "__main__":
    main()
