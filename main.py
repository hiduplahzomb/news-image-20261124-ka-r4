#!/usr/bin/env python3
"""news-image-20261124 entrypoint (standard library only).

Copies the pre-rendered entry.png beside this file to the output
directory and verifies the copy byte for byte. Deterministic: the same
input bytes always produce the same output bytes.
"""
import hashlib
import os
import shutil
import sys

SRC_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)

    with open(src, "rb") as f:
        expected = f.read()
    if len(expected) > 1048576:
        sys.exit("entry.png exceeds 1 MiB: %d bytes" % len(expected))
    if not expected.startswith(b"\x89PNG\r\n\x1a\n"):
        sys.exit("entry.png is not a PNG")

    with open(dst, "wb") as f:
        f.write(expected)

    with open(dst, "rb") as f:
        actual = f.read()
    if hashlib.sha256(actual).hexdigest() != hashlib.sha256(expected).hexdigest():
        sys.exit("output bytes do not match entry.png")
    print("entry.png: %d bytes sha256=%s" % (len(actual),
          hashlib.sha256(actual).hexdigest()))


if __name__ == "__main__":
    main()
