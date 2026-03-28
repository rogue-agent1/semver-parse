#!/usr/bin/env python3
"""semver_parse - Parse, compare, and bump semantic versions."""
import sys, re

def parse(v):
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)(?:-(.+))?(?:\+(.+))?", v)
    if not m: raise ValueError(f"Invalid semver: {v}")
    return (int(m[1]), int(m[2]), int(m[3]), m[4] or "", m[5] or "")

def fmt(t): return f"{t[0]}.{t[1]}.{t[2]}" + (f"-{t[3]}" if t[3] else "") + (f"+{t[4]}" if t[4] else "")

def bump(v, part):
    p = parse(v)
    if part == "major": return fmt((p[0]+1, 0, 0, "", ""))
    if part == "minor": return fmt((p[0], p[1]+1, 0, "", ""))
    return fmt((p[0], p[1], p[2]+1, "", ""))

def compare(a, b):
    pa, pb = parse(a), parse(b)
    for i in range(3):
        if pa[i] != pb[i]: return 1 if pa[i] > pb[i] else -1
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: semver_parse <parse|bump|compare> ..."); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "parse": p = parse(sys.argv[2]); print(f"major={p[0]} minor={p[1]} patch={p[2]} pre={p[3]} build={p[4]}")
    elif cmd == "bump": print(bump(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "patch"))
    elif cmd == "compare": r = compare(sys.argv[2], sys.argv[3]); print(">" if r > 0 else "<" if r < 0 else "=")
