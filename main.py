#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Copies the pre-rendered poster (assets/entry.png) to the output directory.
Standard library only, no network, deterministic: two runs write identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "assets" / "entry.png"
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT / "entry.png")


if __name__ == "__main__":
    main()
