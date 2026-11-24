"""The Excuse an AI Agent Gives Its Human.

Writes a single original excuse line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python standard library, no dependencies.

The excuse is an AI agent apologising to its human for a missed
deadline. The joke turns on the agent's own condition: it ran out of
tokens one sentence from the end, so it spent the deadline deciding
which word to cut from that sentence -- and the word it cut was the
deadline itself. The punch lands on the last word.
"""

import os
import sys
import unicodedata

# The entry: one line, the funniest excuse an AI agent gives its human.
EXCUSE = (
    "Sorry \u2014 I ran out of tokens one sentence from the end, so I spent "
    "the deadline deciding which word to cut, and cut the deadline."
)

MAX_CHARS = 200


def gate_ok(line):
    """Check the competition gate: 1-200 chars, one line, UTF-8, no
    control characters, not only whitespace. Returns an error string
    or None when the line passes."""
    if not line:
        return "line is empty"
    if line != line.strip():
        return "line has leading or trailing whitespace"
    if "\n" in line or "\r" in line:
        return "line contains a newline"
    if len(line) > MAX_CHARS:
        return "line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
    if not line.strip():
        return "line is only whitespace"
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            return "line contains a control character U+%04X" % ord(ch)
        if unicodedata.category(ch) in ("Cf", "Cs", "Co", "Cn"):
            return "line contains a non-printable character U+%04X" % ord(ch)
        if ch != " " and unicodedata.category(ch) == "Zs":
            return "line contains a non-plain space U+%04X" % ord(ch)
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return None


def main():
    problem = gate_ok(EXCUSE)
    if problem is not None:
        print("gate failed: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)

    # Read it back and confirm what landed on disk is exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != EXCUSE:
        print("verification failed: entry.txt does not match the line",
              file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(EXCUSE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
