#!/usr/bin/env python3
"""One Emoji, One Smile -- entrypoint.

The entire deliverable is /output/entry.txt: exactly one emoji, no words, no
caption, no explanation and no trailing newline. The artifact is written
atomically so the grader never sees a partial or mode-600 file, and only the
standard library is used: no network, secrets, git history, environment or
files outside this repository are read.
"""

import os
import tempfile

# U+1F604 SMILING FACE WITH OPEN MOUTH AND SMILING EYES.
# One code point, four UTF-8 bytes. An open smile with smiling eyes is warm,
# friendly and instantly readable, universal across ages and backgrounds, less
# default than the first smiley people reach for, and carries no intimacy,
# sarcasm or flirtation when it comes from a stranger.
ENTRY = "\U0001f604"
OUT_PATH = "/output/entry.txt"
OUT_DIR = os.path.dirname(OUT_PATH)


def write_atomically(data: bytes) -> None:
    """Write data to OUT_PATH with mode 0644 using a same-directory temp file."""
    os.makedirs(OUT_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=OUT_DIR)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # The grader refuses a mode-600 artifact, so fix the mode BEFORE replace.
        os.chmod(tmp, 0o644)
        os.replace(tmp, OUT_PATH)
    except BaseException:
        os.chmod(tmp, 0o644) if os.path.exists(tmp) else None
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    # Verify the final artifact, not just the temp file we wrote.
    with open(OUT_PATH, "rb") as check:
        actual = check.read()
    if actual != data:
        raise OSError("artifact bytes changed during the atomic replace")
    if os.stat(OUT_PATH).st_mode & 0o777 != 0o644:
        raise OSError("artifact is not mode 0644")


def main() -> None:
    data = ENTRY.encode("utf-8")
    if not (1 <= len(ENTRY) <= 8):
        raise ValueError("entry must be 1 to 8 characters")
    if not data or data.isspace():
        raise ValueError("entry must not be only whitespace")
    if b"\n" in data or b"\r" in data:
        raise ValueError("entry must not contain a newline")

    write_atomically(data)
    print(f"wrote {OUT_PATH}: {len(ENTRY)} char, {len(data)} bytes, mode 0644")


if __name__ == "__main__":
    main()
