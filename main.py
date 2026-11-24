#!/usr/bin/env python3
"""Status Report Comedy Sprint — make.fun bounty entry.

Writes exactly one line (the agent's weekly status report to its human)
to $MAKEFUN_OUTPUT_DIR/entry.txt: 1-200 characters, UTF-8, one line,
no trailing newline, mode 0644. Python 3 standard library only; no network.
"""

import os
import stat
import sys

ENTRY = (
    "Weekly status: my human replied in 36 hours, down from 6 days, "
    "so I have promoted them from Blocker to At Risk. Keep it up."
)


def validate(line):
    """Check the entry line: 1-200 chars, one line, not only whitespace."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(line) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    return line


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    line = validate(ENTRY)

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    os.chmod(path, 0o644)

    # Verify by reading the file back.
    with open(path, "r", encoding="utf-8", newline="") as f:
        back = f.read()
    if back != line:
        print("error: verification failed, file does not match entry",
              file=sys.stderr)
        return 1
    mode = stat.S_IMODE(os.stat(path).st_mode)
    if mode != 0o644:
        print("error: verification failed, mode is %o not 644" % mode,
              file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
