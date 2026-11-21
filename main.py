#!/usr/bin/env python3
"""The World - 21 November 2026.

Copies the entry image (entry.png, stored next to this file) to
/output/entry.png. Standard library only; the copy is byte-for-byte, so
repeated runs write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
