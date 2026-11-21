#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png, deterministically.

Reads the image sitting next to this script, streams it to /output
(creating the directory if needed), then verifies the written file by
comparing its size and SHA-256 digest against the source. Exits
non-zero with a clear error if the copy does not match.
"""

import hashlib
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST = Path("/output/entry.png")
CHUNK_SIZE = 65536


def digest(path: Path) -> tuple[int, str]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
            size += len(chunk)
    return size, hasher.hexdigest()


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1

    expected_size, expected_hash = digest(SOURCE)

    DEST.parent.mkdir(parents=True, exist_ok=True)
    with SOURCE.open("rb") as src, DEST.open("wb") as dst:
        while chunk := src.read(CHUNK_SIZE):
            dst.write(chunk)

    actual_size, actual_hash = digest(DEST)
    if (actual_size, actual_hash) != (expected_size, expected_hash):
        print(
            f"error: copy verification failed: "
            f"source {expected_size} bytes sha256 {expected_hash}, "
            f"wrote {actual_size} bytes sha256 {actual_hash}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {DEST} ({actual_size} bytes, sha256 {actual_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
