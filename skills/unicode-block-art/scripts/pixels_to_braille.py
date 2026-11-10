#!/usr/bin/env python3
"""Convert a pixel mask to Braille art. '#' = dot, '.' or space = empty.

Each Braille cell covers 2 columns x 4 rows of pixels; the mask is padded to fit.
"""
import argparse
import sys

# (x, y) inside the 2x4 cell -> dot bit
BITS = {
    (0, 0): 0x01, (0, 1): 0x02, (0, 2): 0x04, (0, 3): 0x40,
    (1, 0): 0x08, (1, 1): 0x10, (1, 2): 0x20, (1, 3): 0x80,
}


def convert(lines, blank):
    rows = [line.rstrip("\n") for line in lines]
    while rows and not rows[-1].strip(" ."):
        rows.pop()
    if not rows:
        return []
    w = max(len(r) for r in rows)
    out = []
    for top in range(0, len(rows), 4):
        cells = []
        for left in range(0, w, 2):
            bits = 0
            for (dx, dy), bit in BITS.items():
                y, x = top + dy, left + dx
                if y < len(rows) and x < len(rows[y]) and rows[y][x] == "#":
                    bits |= bit
            cells.append(chr(0x2800 + bits) if bits else blank)
        out.append("".join(cells).rstrip(" "))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", nargs="?", help="mask file (default: stdin)")
    p.add_argument("--space", action="store_true",
                   help="write empty cells as ASCII spaces instead of the Braille blank U+2800")
    args = p.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    bad = sorted({ch for line in lines for ch in line.rstrip("\n") if ch not in "#. "})
    if bad:
        print(f"error: mask may only contain '#', '.', and space; found {''.join(bad)!r}", file=sys.stderr)
        return 1
    print("\n".join(convert(lines, " " if args.space else "⠀")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
