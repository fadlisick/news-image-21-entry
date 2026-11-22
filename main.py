"""Entrypoint: deliver the poster image to the grader output dir.

Stdlib only. Validates the committed entry.png (PNG, 1024x1024,
at most 1 MiB), copies it to MAKEFUN_OUTPUT_DIR/entry.png and makes
the file world-readable. Never touches the output directory itself.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576


def main():
    os.umask(0o022)
    with open(SRC, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG")
    if data[12:16] != b"IHDR":
        sys.exit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        sys.exit("entry.png is not 1024x1024")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(outdir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    os.chmod(dest, 0o644)
    print("wrote %s (%d bytes, 1024x1024)" % (dest, len(data)))


if __name__ == "__main__":
    main()
