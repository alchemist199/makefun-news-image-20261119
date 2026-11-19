#!/usr/bin/env python3
"""Entrypoint for make.fun news-image-20261119.

Copies the pre-drawn front page (entry.png, built by build_frontpage.py)
to /output/entry.png, after verifying the PNG is whole and byte-identical
to the recorded hash. Standard library only, no network, deterministic.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = (
    "b1a5f7b7d8987b4e8c7311a8d33e51ae034a0af1a3a56c9e15fdfe207fdf3088"
)
EXPECTED_SIZE = 138366
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def verify_png(data):
    """Check magic bytes, IHDR dimensions, and a trailing IEND chunk."""
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        fail("not a PNG file (bad magic bytes)")
    if len(data) > MAX_BYTES:
        fail("PNG is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 33:
        fail("PNG too short to hold an IHDR chunk")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        fail("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (width, height))
    # Walk every chunk: verify each CRC and that the file ends with IEND.
    pos = 8
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            fail("chunk %r overruns the file" % ctype)
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        actual_crc = zlib.crc32(ctype + data[pos + 8:pos + 8 + length])
        if stored_crc != (actual_crc & 0xFFFFFFFF):
            fail("chunk %r has a bad CRC" % ctype)
        if ctype == b"IEND":
            if length != 0 or end != len(data):
                fail("trailing data after IEND chunk")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        fail("PNG does not end with a valid IEND chunk")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % digest)
    if len(data) != EXPECTED_SIZE:
        fail("size mismatch: got %d, expected %d"
             % (len(data), EXPECTED_SIZE))
    return digest


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read entry.png: %s" % exc)
    digest = verify_png(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    print("wrote %s (%d bytes, sha256 %s)"
          % (out_path, len(data), digest))


if __name__ == "__main__":
    main()
