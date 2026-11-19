#!/usr/bin/env python3
"""make.fun entry for the news-image-20261118 bounty.

The entry image (entry.png, a 1024x1024 newspaper-style summary of the
world news of Wednesday 18 November 2026) is rendered ahead of time by
build_image.py and shipped in this repository. This program only copies it
to the output directory the grader provides, so the graded run needs no
network and is fully deterministic: the same bytes come out every time.
"""

import os
import shutil
import sys

ENTRY_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, ENTRY_NAME)
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
