#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 bounty.

Pure standard library: copies the repository's news-frontpage.png to
the output path. The source image is located relative to this file,
never relative to the current working directory, so it works from a
read-only repo mount and any cwd. Deterministic: repeated runs write
identical bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news-frontpage.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        dst = os.path.join(out_dir, "entry.png")
    elif os.path.isdir("/output"):
        dst = "/output/entry.png"
    else:
        dst = os.path.join(os.getcwd(), "entry.png")

    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
