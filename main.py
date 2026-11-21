#!/usr/bin/env python3
"""Copy the pre-built entry.png next to this file into the output dir.

Standard library only, no network. Deterministic: the output bytes are
exactly the bytes of the bundled entry.png.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        raise SystemExit(1)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print(f"copied entry.png ({os.path.getsize(dest)} bytes) to {dest}")


if __name__ == "__main__":
    main()
