#!/usr/bin/env python3
"""Render quadrant block art with background fills so rows join without gaps.

Each cell's background takes its majority colour; only the minority quadrants
are drawn as a glyph in the other colour. Full cells become coloured spaces.
Ties go to a transparent colour if there is one, otherwise to the hole.
Space, █ ▀ ▄ ▌ ▐ and the quadrants ▖▗▘▙▚▛▜▝▞▟ are block art; space is the
hole. Any other character (letters, digits, '-', CJK, …) is text: it keeps its
glyph and is drawn in the ink colour on the hole colour. Tabs and control
characters are rejected. Lines starting with ``` are skipped.

Line prefixes: <org> keeps ink/hole colours, <inv> swaps them. Untagged lines
also swap them. Prefixes are removed and affect only their own line; background
fill conversion still applies in both modes.

Colours: an SGR foreground code (30-37, 90-97), #rrggbb, or 'default' for the
terminal's own background (transparent). At most one colour may be 'default'.
A transparent glyph is drawn with reverse video, which paints the terminal's
background colour as a solid fill.
"""
import argparse
import json
import sys
import unicodedata

# Quadrant bitmask: upper-left 8, upper-right 4, lower-left 2, lower-right 1.
MASK = {" ": 0, "▗": 1, "▖": 2, "▄": 3, "▝": 4, "▐": 5, "▞": 6, "▟": 7,
        "▘": 8, "▚": 9, "▌": 10, "▙": 11, "▀": 12, "▜": 13, "▛": 14, "█": 15}
GLYPH = {m: g for g, m in MASK.items()}


def sgr(spec, background):
    if spec == "default":
        return "49" if background else "39"
    if spec.startswith("#") and len(spec) == 7:
        try:
            r, g, b = (int(spec[i:i + 2], 16) for i in (1, 3, 5))
        except ValueError:
            raise ValueError(f"colour {spec!r}: not a #rrggbb hex colour") from None
        return f"{48 if background else 38};2;{r};{g};{b}"
    code = int(spec) if spec.isdigit() else 0
    if not (30 <= code <= 37 or 90 <= code <= 97):
        raise ValueError(f"colour {spec!r}: use 30-37, 90-97, #rrggbb or default")
    return str(code + 10 if background else code)


def cell(ch, tie):
    """Return (glyph, glyph colour, background colour) as 'ink'/'hole' labels."""
    if ch not in MASK:  # text
        return ch, "ink", "hole"
    ink = MASK[ch]
    count = bin(ink).count("1")
    if count > 2 or (count == 2 and tie == "ink"):
        return GLYPH[15 ^ ink], "hole", "ink"
    return GLYPH[ink], "ink", "hole"


def paint(glyph, fg_role, bg_role, colours):
    bg = sgr(colours[bg_role], True)
    if glyph == " ":
        codes = bg
    elif colours[fg_role] == "default":
        # Reverse video: the glyph takes the default background, the cell takes the colour.
        codes = f"7;{sgr(colours[bg_role], False)};49"
    else:
        codes = f"{sgr(colours[fg_role], False)};{bg}"
    return f"\x1b[0;{codes}m{glyph}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?", help="UTF-8 art file (default or '-': stdin)")
    p.add_argument("--ink", default="36", help="shape colour (default 36, cyan; 'default' = transparent)")
    p.add_argument("--hole", default="30", help="hole colour (default 30, black; 'default' = transparent)")
    p.add_argument("--json", action="store_true", help="print per-cell glyph/fg/bg instead of ANSI")
    args = p.parse_args()

    if args.file and args.file != "-":
        text = open(args.file, encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    rows = [line for line in text.lstrip("﻿").splitlines() if not line.startswith("```")]
    for n, line in enumerate(rows, 1):
        for col, ch in enumerate(line, 1):
            if unicodedata.category(ch) == "Cc":
                print(f"error: line {n} col {col}: control character U+{ord(ch):04X}"
                      + (" (tab), use spaces" if ch == "\t" else ""), file=sys.stderr)
                return 1

    colours = {"ink": args.ink, "hole": args.hole}
    try:
        for spec in colours.values():
            sgr(spec, False)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if args.ink == args.hole == "default":
        print("error: only one of --ink and --hole can be default", file=sys.stderr)
        return 1
    cells = []
    for line in rows:
        inverted = not line.startswith("<org>")
        if line.startswith(("<org>", "<inv>")):
            line = line[5:]
        roles = {"ink": "hole", "hole": "ink"} if inverted else {"ink": "ink", "hole": "hole"}
        tie = "ink" if colours[roles["ink"]] == "default" else "hole"
        cells.append([(g, roles[f], roles[b]) for g, f, b in (cell(ch, tie) for ch in line)])
    if args.json:
        print(json.dumps([[dict(zip(("glyph", "fg", "bg"), c)) for c in row] for row in cells],
                         ensure_ascii=False))
        return 0

    for row in cells:
        print("".join(paint(g, f, b, colours) for g, f, b in row) + "\x1b[0m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
