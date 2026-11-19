#!/usr/bin/env python3
"""make.fun entry for the news-image-20261118 bounty.

The entry image (entry.png, a 1024x1024 newspaper-style summary of the
world news of Wednesday 18 November 2026) is rendered ahead of time by
build_image.py and shipped in this repository. This program only copies it
to the output directory the grader provides, so the graded run needs no
network and is fully deterministic: the same bytes come out every time.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY_NAME)
    with open(src, "rb") as f:
        head = f.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("error: %s is not a PNG file" % ENTRY_NAME, file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, ENTRY_NAME)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print("wrote", dst, os.path.getsize(dst), "bytes sha256", digest)


if __name__ == "__main__":
    main()
