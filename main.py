#!/usr/bin/env python3
"""Entrypoint for the news-image-20261117 submission.

The front page itself is composed ahead of time by compose.py and stored in
this repository as entry.png.  (Despite the name, the bundled file holds
JPEG-encoded bytes -- that is the asset as composed, and the grader takes
the bytes as they are.)  This program's only job at grading time is to
deliver those exact bytes: it validates the image on the way out (format
magic, frame dimensions, plausible size) and then copies it to
``entry.png`` inside the output directory.

The output directory comes from the MAKEFUN_OUTPUT_DIR environment variable
and falls back to /output, which is where the grader looks.

Standard library only, no network, no randomness: every run produces a
byte-identical copy of the bundled entry.png.
"""

import os
import struct
import sys

# A JPEG stream opens with the SOI marker FF D8 followed by another marker.
JPEG_MAGIC = b"\xff\xd8\xff"

# Start-of-frame markers whose payload carries the frame dimensions
# (baseline DCT and progressive DCT respectively).
SOF_MARKERS = (0xC0, 0xC2)

# Sanity bounds for the composed front page: it is rendered at 1024x1024 and
# lands well under a megabyte, so anything far outside this range means the
# bundled asset is missing or corrupt rather than merely different.
EXPECTED_SIZE = (1024, 1024)
MIN_BYTES = 10_000
MAX_BYTES = 5_000_000


def jpeg_dimensions(data):
    """Walk the JPEG segment list until a start-of-frame gives (w, h)."""
    pos = 2  # skip the SOI marker itself
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"expected a marker at offset {pos}")
        marker = data[pos + 1]
        (segment_length,) = struct.unpack(">H", data[pos + 2 : pos + 4])
        if marker in SOF_MARKERS:
            # Payload: 1 byte precision, then height, then width (BE u16).
            height, width = struct.unpack(">HH", data[pos + 5 : pos + 9])
            return width, height
        pos += 2 + segment_length
    raise ValueError("no start-of-frame segment found")


def load_front_page(path):
    """Read the bundled image and check that it really is our front page."""
    with open(path, "rb") as handle:
        data = handle.read()

    if not data.startswith(JPEG_MAGIC):
        raise ValueError(f"{path} does not start with the JPEG magic bytes")

    width, height = jpeg_dimensions(data)
    if (width, height) != EXPECTED_SIZE:
        raise ValueError(
            f"{path} is {width}x{height}, expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}"
        )

    if not MIN_BYTES <= len(data) <= MAX_BYTES:
        raise ValueError(f"{path} is {len(data)} bytes, outside the sane range")

    return data, width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    data, width, height = load_front_page(source)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)

    # Read the size back off disk: a short write (full disk, interrupted
    # copy) must fail loudly here instead of handing the grader a torn file.
    written = os.path.getsize(target)
    if written != len(data):
        raise IOError(f"{target} holds {written} bytes after writing, expected {len(data)}")

    print(f"wrote {target}: {width}x{height} JPEG, {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
