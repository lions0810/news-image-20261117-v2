#!/usr/bin/env python3
"""Entry program for the news-image-20261117 bounty (V2: the broadside).

Copies the pre-composed entry.png (built by compose.py, stored beside this
script) to the output directory given by MAKEFUN_OUTPUT_DIR
(default /output). Deterministic: the same input bytes are copied every run.
Standard library only.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")


if __name__ == "__main__":
    main()
